import yaml

def read_config(clf_name):
    with open('config/%s.yaml' % clf_name) as f:
        clf_config = yaml.load(f)
    return clf_config
