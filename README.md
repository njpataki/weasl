# weasl

A framework for building weakly supervised machine learning pipelines. Instead of hand-labeling thousands of examples, you write heuristic rules that generate noisy labels automatically, then train classifiers on top of them.

## Concept

Traditional supervised learning requires expensive hand-labeled data. Weak supervision flips this: you write rules (e.g. regex patterns, keyword lists) that imperfectly label your data, then train a classifier on those noisy labels. The classifier generalizes beyond the rules.

```
raw data → rules → weak labels → classifier → predictions
```

weasl provides the scaffolding to organize and run this pipeline from the command line.

## Installation

```bash
pip install .
# or for development
pip install -e ".[dev]"
```

Requires Python 3.8+.

## Usage

### 1. Create a project

```bash
weasl startproject myproject
```

Creates a standard directory structure:

```
myproject/
├── config/
├── rules/
├── featurizers/
├── classifiers/
├── curated_labels/
├── data/
│   ├── training_sets/
│   └── test_sets/
└── tmp/
    └── serialized_models/
```

### 2. Add a classifier

```bash
cd myproject
weasl startclassifier spam
```

Creates stub files for you to fill in:

```
rules/spam.py
featurizers/spam.py
classifiers/spam.py
config/spam.yaml
```

### 3. Define your rules

Edit `rules/spam.py`. Rules are callables that take a DataFrame and return a label Series. The built-in `RegexInFieldsRule` is a good starting point:

```python
from weasl.rules import RegexInFieldsRule

is_spam = RegexInFieldsRule(fields=['subject', 'body'], rgx='buy now|click here|free offer')
is_not_spam = RegexInFieldsRule(fields=['subject'], rgx='re:|fwd:', invert=True)
```

### 4. Define your features

Edit `featurizers/spam.py`. Feature functions take a DataFrame and return a DataFrame of features:

```python
import pandas as pd

def text_length(df):
    return pd.DataFrame({'char_count': df['body'].str.len()})
```

### 5. Define your classifier

Edit `classifiers/spam.py`. Any sklearn-compatible class works:

```python
from sklearn.linear_model import LogisticRegression

class SpamClassifier(LogisticRegression):
    pass
```

### 6. Configure and train

Edit `config/spam.yaml` to wire everything together:

```yaml
rules:
  - spam.is_spam
features:
  - spam.text_length
classifiers:
  - spam.SpamClassifier
```

Then train:

```bash
weasl train spam --train-file data/training_sets/emails.csv
```

Trained models are serialized to `tmp/serialized_models/`.

## Running tests

```bash
pytest
```

## Architecture

| Module | Role |
|--------|------|
| `main.py` | CLI entry point, routes subcommands |
| `commands.py` | Implements `startproject`, `startclassifier`, `train` |
| `rules.py` | `Rule` base class and `RegexInFieldsRule` |
| `features.py` | Calls feature functions and concatenates results |
| `config.py` | Reads YAML config files |
| `project_env.py` | Dynamically imports user-defined rules/features/classifiers |
| `regex.py` | Punctuation-aware regex matching |
| `utils.py` | Filesystem helpers |

## License

MIT
