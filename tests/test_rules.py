import pandas as pd
import numpy as np
import pytest
from weasl.rules import RegexInFieldsRule


def make_df(texts, col='text'):
    return pd.DataFrame({col: texts})


def test_match_gives_label_one():
    rule = RegexInFieldsRule(fields=['text'], rgx='cat')
    df = make_df(['the cat sat', 'nothing here'])
    labels = rule(df)
    assert labels[0] == 1
    assert labels[1] == 0


def test_no_match_gives_label_zero():
    rule = RegexInFieldsRule(fields=['text'], rgx='xyz')
    df = make_df(['hello world', 'goodbye'])
    labels = rule(df)
    assert all(labels == 0)


def test_invert_flips_labels():
    rule = RegexInFieldsRule(fields=['text'], rgx='cat', invert=True)
    df = make_df(['the cat sat', 'nothing here'])
    labels = rule(df)
    assert labels[0] == 0
    assert labels[1] == 1


def test_match_in_any_field_gives_label_one():
    rule = RegexInFieldsRule(fields=['title', 'body'], rgx='urgent')
    df = pd.DataFrame({'title': ['hello', 'urgent matter'], 'body': ['urgent fix needed', 'nothing']})
    labels = rule(df)
    assert labels[0] == 1  # match in body
    assert labels[1] == 1  # match in title


def test_returns_series_of_correct_length():
    rule = RegexInFieldsRule(fields=['text'], rgx='x')
    df = make_df(['a', 'b', 'c', 'd', 'e'])
    labels = rule(df)
    assert len(labels) == 5
