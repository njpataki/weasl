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

    # use execute method to execute all the private methods 

    def _get_feature_functions(self, clargs):

        # construct path to feature_functions
        # use project_env.get_fucntions to get a lsit of feature functions availabel
        # use feautures module to get a feature matrix

        config_dict = config.read_config(clargs.name)
        featurizer = config_dict['featurizers'] 
        clf = config_dict['classifier']

    def _build_clf():
        # construct path to clfr
        # use project_env.get_class(path_to_clf_str)
        # instantiate the clf
        pass

    def _fit():
        # for each set of labels return a fitted classier in a list
        pass
        
    def _label_samples():
        # use labels.py to return a df of labels

    def _serialize():
        # serialize all the clfrs to disc using conventions in google sheet
        pass

    def execute(self, clargs):
        pass

