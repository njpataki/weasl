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
        dirs = ['rules', 'generators', 'featurizers', 'classifiers', 'evaluation']
        utils.create_dir_structure([os.path.join(clargs.name, dir) for dir in dirs])

class StartClassifier(Command):

    def setup_clparser(self, parser):
        parser.add_argument('name', type=str, help='Name of the classifier')
        return parser

    def execute(self, clargs):
        dirs = ['rules', 'generators', 'featurizers', 'classifiers', 'evaluation']
        utils.create_dir_structure([os.path.join(dir, '%s.py' % clargs.name) for dir in dirs])
