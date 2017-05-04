from . import regex

class Rule(object):
    def run(self, samples):
        raise NotImplementedError('Rule method run not implemented')

class RegexInFieldsRule(rule):

    def __init__(self, fields, rgx, invert=False):
        self.fields = fields
        self.rgx = rgx
        self.invert = invert

    def run(self, samples):
        labels = pd.Series(np.zeros(samples.shape[0]))
        for i, s in samples.iterrows():
            for field in self.fields:
                if regex.regex_search(self.rgx, s[field]):
                    labels[i] = 1
                    break
        if self.invert:
            return 1 - labels
        else:
            return labels
