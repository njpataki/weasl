import pandas as pd
import pytest
from weasl.features import call_and_concat


def length_feature(df):
    return pd.DataFrame({'length': df['text'].str.len()})


def word_count_feature(df):
    return pd.DataFrame({'words': df['text'].str.split().str.len()})


def test_single_feature_function():
    df = pd.DataFrame({'text': ['hello world', 'hi']})
    result = call_and_concat(df, [length_feature])
    assert result.shape == (2, 1)


def test_multiple_feature_functions_concat():
    df = pd.DataFrame({'text': ['hello world', 'hi']})
    result = call_and_concat(df, [length_feature, word_count_feature])
    assert result.shape == (2, 2)


def test_columns_are_prefixed_with_module_and_function():
    df = pd.DataFrame({'text': ['hello world']})
    result = call_and_concat(df, [length_feature])
    col = result.columns[0]
    assert 'length_feature' in col
    assert col.endswith('.length')


def test_feature_values_are_correct():
    df = pd.DataFrame({'text': ['hello world', 'hi']})
    result = call_and_concat(df, [length_feature])
    length_col = result.columns[0]
    assert result[length_col].iloc[0] == 11  # 'hello world'
    assert result[length_col].iloc[1] == 2   # 'hi'
