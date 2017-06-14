import importlib
import inspect
import sys
import os

def _get_module(module_name, dir):
    sys.path.append(os.getcwd())
    return importlib.import_module('%s.%s' % (dir, module_name))

def get_functions(module_name, dir):
    module = _get_module(module_name, dir)
    names_functions = inspect.getmembers(module, inspect.isfunction)
    return dict(names_functions)

# TODO: how is class_name collected? From config?
def get_class(classifier_name, dir, class_name):
    module = _get_module(classifier_name, dir)
    class_ = getattr(module, class_name)
    return class_

# def get_function(classifier_name, dir, func_name):
#     module = _get_module(classifier_name, dir)
#     func_ = getattr(module, func_name)
#     return func_
