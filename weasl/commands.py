import os

import pandas as pd

from . import project_env
from . import features
from . import config
from . import utils


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
        utils.create_dir_structure([os.path.join(clargs.name, dir) for dir in dirs])
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
        utils.create_dir_structure([os.path.join(dir, '%s.py' % clargs.name) for dir in dirs])

        dirs = ['config']
        utils.create_dir_structure([os.path.join(dir, '%s.yaml' % clargs.name) for dir in dirs])


class Train(Command):

    def setup_clparser(self, parser):
        parser.add_argument(
            'name', 
            type=str, 
            help='Name of the classifier')
        parser.add_argument(
            '--train-file', 
            type=str, 
            help='Absolute path to training permits')
        return parser

    def _get_feature_functions(self, clargs):
        dirs_module = [('featurizers', 'master'), ('featurizers', clargs.name)]
        names_features = {}
        for dir, module in dirs_module:
            names_features.update(project_env.get_functions(module, dir))
        return names_features.values()

    def _get_rule_functions(self, clargs):
        module, dir = clargs.name, 'rules'
        names_rules = {}
        names_rules.update(project_env.get_functions(module, dir))
        return names_rules.values()

    def _build_clf(self, clargs):
        # construct path to clfr
        # use project_env.get_class(path_to_clf_str)
        # instantiate the clf
        pass

    def _fit(self, training_labels):
        # for each set of labels return a fitted classifier in a list
        # requires a .fit on classifier (sklearn)
        pass
        
    def _label_samples(self):
        # use labels.py to return a df of labels
        pass

    def _serialize(self):
        # serialize all the clfrs to disc using conventions in google sheet
        pass

    def execute(self, clargs):
        train_df = pd.read_csv(clargs.train_file)
        feature_funcs = self._get_feature_functions(clargs)
        train_matrix_df = features.call_and_concat(train_df, feature_funcs)
        rule_funcs = self._get_rule_functions(clargs)
        print rule_funcs
        labels = [rule_func(train_df) for rule_func in rule_funcs]
        print len(labels)
        print labels[0][:10]
        # for y_train in y_trains:
        #     clf = self._build_clf(clargs)

        

