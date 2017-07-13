import pickle
import os

import argparse
import pandas as pd

from . import project_env
from . import features
from . import config
from . import utils
from .evaluation import server

class Command(object):

    def setup_clparser(self, parser):
        return parser

    def execute(self, clargs):
        raise NotImplementedError('Command.execute not implemented!')


class StartProjectCommand(Command):

    def setup_clparser(self, parser):
        parser.add_argument(
            'name', 
            type=str, 
            help='Name of the project')
        return parser

    def execute(self, clargs):
        dirs = ['rules', 
                'config', 
                'curated_labels',
                os.path.join('featurizers', 'master.py'),
                os.path.join('classifiers', 'master.py'),
                os.path.join('data', 'training_sets'),
                os.path.join('data', 'test_sets'),
                os.path.join('tmp', 'serialized_models')]
        utils.create_dir_structure([os.path.join(clargs.name, dir_) for dir_ in dirs])
        # TODO: deprecate master.yaml build
        utils.touch(os.path.join(clargs.name, 'config', 'master.yaml'))


class StartClassifier(Command):

    def setup_clparser(self, parser):
        parser.add_argument(
            'name', 
            type=str, 
            help='Name of the classifier')
        return parser

    def execute(self, clargs):
        dirs = ['rules', 'featurizers', 'classifiers']
        utils.create_dir_structure([os.path.join(dir_, '%s.py' % clargs.name) for dir_ in dirs])

        dirs = ['config']
        utils.create_dir_structure([os.path.join(dir_, '%s.yaml' % clargs.name) for dir_ in dirs])


class Train(Command):

    def setup_clparser(self, parser):
        parser.add_argument(
            'name', 
            type=str, 
            help='arg passed to `weasl startclassifier [name]`')
        parser.add_argument(
            '--train-file', 
            type=str, 
            help='path to training permits')
        return parser

    def _get_rule_functions(self):
        rules_funcs = {}
        for rule_config in self.config['rules']:
            module_name, rule_name = rule_config.split('.')
            rules_func = project_env.get_function(
                dir_='rules', 
                module_name=module_name,
                function_name=rule_name)
            rules_funcs[rule_name] = rules_func
        return rules_funcs

    def _get_feature_functions(self):
        features_funcs = {}
        for feature_config in self.config['features']:
            module_name, feature_name = feature_config.split('.')
            feature_func = project_env.get_function(
                dir_='featurizers', 
                module_name=module_name, 
                function_name=feature_name)
            features_funcs[feature_name] = feature_func
        return features_funcs

    def _build_classifiers(self):
        clfs_classes = {}
        for clf_config in self.config['classifiers']:
            module_name, clf_name = clf_config.split('.')
            clf = project_env.get_class(
                dir_='classifiers', 
                module_name=module_name,
                class_name=clf_name)
            clfs_classes[clf_name] = clf
        return clfs_classes

    @staticmethod
    def _serialize(clargs, rule_name, clf_name, clf):
        train_file = os.path.basename(clargs.train_file).split('.')[0]
        filepath_args = (clargs.name, rule_name, train_file, clf_name)
        filepath = 'tmp/serialized_models/%s__%s__%s__%s.pickle' % filepath_args
        with open(filepath, 'w') as f:
            pickle.dump(clf, f)

    def execute(self, clargs):
        self.config = config.read_config(clargs.name)
        train_df = pd.read_csv(clargs.train_file)
        features_funcs = self._get_feature_functions()
        ftrzd_train_df = features.call_and_concat(train_df, features_funcs.values())
         
        rules_funcs = self._get_rule_functions() 
        clfs_classes = self._build_classifiers()
        for clf_name, clf in clfs_classes.iteritems():
            clf_ = clf()
            for rule_name, rule_func in rules_funcs.iteritems():
                y_train = rule_func(train_df)
                clf_.fit(ftrzd_train_df, y_train) 
                self._serialize(clargs, rule_name, clf_name, clf_)


class Evaluate(Command):

    def setup_clparser(self, parser):
        parser.add_argument(
            'name', 
            type=str, 
            help='arg passed to `weasl startclassifier [name]`')
        parser.add_argument(
            '--evaluation-file',
            type=argparse.FileType('r'),
            help='path to labeled file')
        parser.add_argument(
            '--interactive',
            action='store_true',
            default=False,
            help='spawns the evaluation server for interactive evaluation')
        parser.add_argument(
            '--label-file',
            default=None,
            type=argparse.FileType('r'),
            help='file with curated labels')
        return parser
    
    #TODO This should be done outside the commands module
    def _write_evaluation_metrics(self, eval_df, curated_labels):
        from sklearn.metrics import f1_score
        f1 = f1_score(eval_df['labels'].values, curated_labels.values)
        print('F1 score: %s' % f1)
        
    def execute(self, clargs):
        eval_df = pd.read_csv(clargs.evaluation_file)
        if clargs.interactive:
            app_name = '%s_evaluation' % (clargs.name)
            evaluation_server = server.EvaluationServer(app_name,
                                                        clargs.evaluation_file.name,
                                                        eval_df)
            evaluation_server.run()
            curated_labels = pd.read_csv('curated_labels/%s' % clargs.evaluation_file.name,
                                         index_col=0)
        else:
            if clargs.label_file is not None:
                curated_labels = pd.read_csv(clargs.label_file, index_col=0)
            else:
                raise ValueError('--label-file must be non-null if not running in --interactive mode')
        self._write_evaluation_metrics(eval_df, curated_labels)
