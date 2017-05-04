import yaml

def read_config(classifier_name):
    master_config = yaml.load('config/master.yaml')
    classifier_config = yaml.load('config/%s.yaml' % classifier_name)
    master_config.update(classifier_config)
    return master_config

