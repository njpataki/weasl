# import importlib
import inspect
import imp

def _get_module(module_name, dir):
    path = '%s/%s.py' % (dir, module_name)
    return imp.load_source(module_name, path)

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
