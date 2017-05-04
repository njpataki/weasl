import os

from . import utils


class Command(object):

    def setup_clparser(self, parser):
        return parser

    def execute(self, clargs):
        raise NotImplementedError('Command.execute not implemented!')

class StartProjectCommand(Command):

    def setup_clparser(self, parser):
        parser.add_argument('name', type=str, help='Name of the project')
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
        parser.add_argument('name', type=str, help='Name of the classifier')
        return parser

    def execute(self, clargs):
        dirs = ['rules', 'featurizers', 'classifiers']
        utils.create_dir_structure([os.path.join(dir, '%s.py' % clargs.name) for dir in dirs])

        dirs = ['config']
        utils.create_dir_structure([os.path.join(dir, '%s.yaml' % clargs.name) for dir in dirs])
