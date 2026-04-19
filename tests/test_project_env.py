import os
import sys
import pytest
from weasl import project_env


def test_get_function_returns_callable(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rules_dir = tmp_path / 'rules'
    rules_dir.mkdir()
    (rules_dir / '__init__.py').write_text('')
    (rules_dir / 'myrules.py').write_text(
        'def label_positive(df):\n    return 1\n'
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    fn = project_env.get_function('rules', 'myrules', 'label_positive')
    assert callable(fn)
    assert fn(None) == 1


def test_get_function_missing_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rules_dir = tmp_path / 'rules'
    rules_dir.mkdir()
    (rules_dir / '__init__.py').write_text('')
    (rules_dir / 'myrules.py').write_text('def label_positive(df):\n    return 1\n')
    monkeypatch.syspath_prepend(str(tmp_path))

    with pytest.raises(KeyError):
        project_env.get_function('rules', 'myrules', 'nonexistent_func')


def test_get_class_returns_class(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    clfs_dir = tmp_path / 'classifiers'
    clfs_dir.mkdir()
    (clfs_dir / '__init__.py').write_text('')
    (clfs_dir / 'myclf.py').write_text(
        'class MyClassifier:\n    def fit(self, X, y): pass\n'
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    cls = project_env.get_class('classifiers', 'myclf', 'MyClassifier')
    assert cls.__name__ == 'MyClassifier'
    assert hasattr(cls(), 'fit')


def test_get_class_missing_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    clfs_dir = tmp_path / 'classifiers'
    clfs_dir.mkdir()
    (clfs_dir / '__init__.py').write_text('')
    (clfs_dir / 'myclf.py').write_text('class MyClassifier: pass\n')
    monkeypatch.syspath_prepend(str(tmp_path))

    with pytest.raises(KeyError):
        project_env.get_class('classifiers', 'myclf', 'NoSuchClass')
