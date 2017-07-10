import importlib
import inspect
import sys
import os

def _get_module(dir_, module_name):
    sys.path.append(os.getcwd())
    return importlib.import_module('%s.%s' % (dir_, module_name))

def get_functions(dir_, module_name):
    module = _get_module(dir_, module_name)
    names_functions = inspect.getmembers(module, inspect.isfunction)
    return dict(names_functions)

def get_function(dir_, module_name, function_name):
    names_functions = get_functions(dir_, module_name)
    return names_functions[function_name]

def get_classes(dir_, module_name):
    module = _get_module(dir_, module_name)
    names_classes = inspect.getmembers(module, inspect.isclass)
    return dict(names_classes)

def get_class(dir_, module_name, class_name):
    names_classes = get_classes(dir_, module_name)
    return names_classes[class_name]
