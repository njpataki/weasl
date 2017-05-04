import os

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
                os.path.join('data', 'training_sets'),
                os.path.join('data', 'test_sets'),
                os.path.join('tmp', 'serialized_models')]
        utils.create_dir_structure([os.path.join(clargs.name, dir) for dir in dirs])
        os.mknod(os.path.join(clargs.name, 'config', 'master.yaml'))

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

    def set_up(self, clargs):

        # construct path to feature_functions
        # use eval(feature_func_string) 
        # execture feature_func to get data
        # hstack the results of these feature functions

        # construct path to clfr
        # use eval(clf_str)
        # pass the featurized train_matrix

        # access user-defined rules in rules.py
        # apply these rules and create labels using pre-defined labeling module

        # fit with rule_based_labels, train_matrix

        # return trained_clf

        config_dict = config.read_config(clargs.name)
        featurizer = config_dict['featurizers'] 
        clf = config_dict['classifier']


        

    def execute(self, clargs):

        set_up()
        fit()
        predict()


    def fit(self):
        
        raise NotImplementedError()

    def predict(self):
        raise NotImplementedError()
