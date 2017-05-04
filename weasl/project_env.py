import importlib


def _get_module(classifier_name, dir):
    module_name = '%s.%s' % (dir, classifier_name)
    return importlib.import_module(module_name)

def get_class(classifier_name, dir, class_name):
    module = _get_module(classifier_name, dir)
    class_ = getattr(module, class_name)
    return class_

def get_function(classifier_name, dir, func_name):
    module = _get_module(classifier_name, dir)
    func_ = getattr(module, func_name)
    return func_
