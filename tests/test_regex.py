import numpy as np
import pytest
from weasl.regex import regex_search, _match_regex


def test_string_match():
    assert regex_search('hello', 'say hello world') is True


def test_string_no_match():
    assert regex_search('xyz', 'say hello world') is False


def test_string_case_insensitive():
    assert regex_search('hello', 'SAY HELLO WORLD') is True


def test_string_at_start_of_text():
    assert regex_search('hello', 'hello world') is True


def test_string_after_punctuation():
    assert regex_search('hello', 'well,hello there') is True


def test_array_returns_ndarray():
    result = regex_search('hello', ['say hello', 'goodbye'])
    assert isinstance(result, np.ndarray)


def test_array_correct_matches():
    result = regex_search('cat', ['the cat sat', 'no match here', 'cat'])
    np.testing.assert_array_equal(result, [True, False, True])


def test_array_all_false():
    result = regex_search('xyz', ['hello', 'world'])
    np.testing.assert_array_equal(result, [False, False])


def test_array_all_true():
    result = regex_search('yes', ['yes please', 'oh yes', 'yes'])
    np.testing.assert_array_equal(result, [True, True, True])
