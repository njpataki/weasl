import argparse
from . import commands


def top_level_command():
    
    COMMANDS = {'startproject': commands.StartProjectCommand(), 
                'startclassifier': commands.StartClassifier()}

    parser = argparse.ArgumentParser(
        prog='weasl', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    subparsers = parser.add_subparsers(help='sub-command helps')

    for command, handler in COMMANDS.iteritems():
        command_subparser = subparsers.add_parser(command)
        command_subparser.set_defaults(handler=handler)
        command_subparser = handler.setup_clparser(command_subparser)
    
    clargs = parser.parse_args()
    clargs.handler.execute(clargs)
