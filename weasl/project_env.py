import importlib
import inspect

def _get_module(module_name, dir):
    return importlib.import_module('%s.%s' % (dir, module_name))

def get_functions(module_name, dir):
    module = _get_module(module_name, dir)
    names_functions = inspect.getmembers(module, inspect.isfunction)
    print names_functions
    return dict(names_functions)

def get_class(classifier_name, dir, class_name):
    module = _get_module(classifier_name, dir)
    class_ = getattr(module, class_name)
    return class_

# def get_function(classifier_name, dir, func_name):
#     module = _get_module(classifier_name, dir)
#     func_ = getattr(module, func_name)
#     return func_
