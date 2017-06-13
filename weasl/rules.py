import pandas as pd
import numpy as np

from . import regex

class Rule(object):
    def __call__(self, samples_df):
        raise NotImplementedError('Rule method __call__ not implemented')

class RegexInFieldsRule(Rule):

    def __init__(self, fields, rgx, invert=False):
        self.fields = fields
        self.rgx = rgx
        self.invert = invert

    def __call__(self, samples_df):
        labels = pd.Series(np.zeros(samples_df.shape[0]))
        for i, s in samples_df.iterrows():
            for field in self.fields:
                if regex.regex_search(self.rgx, s[field]):
                    labels[i] = 1
                    break
        if self.invert:
            labels = 1 - labels
        return labels
