import os
import pytest
from unittest.mock import patch
from weasl.commands import StartProjectCommand, StartClassifier


class FakeArgs:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_startproject_creates_expected_directories(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cmd = StartProjectCommand()
    cmd.execute(FakeArgs(name='myproject'))

    expected_dirs = [
        'myproject/rules',
        'myproject/config',
        'myproject/curated_labels',
        'myproject/data/training_sets',
        'myproject/data/test_sets',
        'myproject/tmp/serialized_models',
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f'Expected directory missing: {d}'


def test_startproject_creates_master_yaml(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    StartProjectCommand().execute(FakeArgs(name='myproject'))
    assert os.path.isfile('myproject/config/master.yaml')


def test_startproject_creates_master_py_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    StartProjectCommand().execute(FakeArgs(name='myproject'))
    assert os.path.isfile('myproject/featurizers/master.py')
    assert os.path.isfile('myproject/classifiers/master.py')


def test_startclassifier_creates_py_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # create the directories startproject would have made
    for d in ['rules', 'featurizers', 'classifiers', 'config']:
        os.makedirs(d, exist_ok=True)
    StartClassifier().execute(FakeArgs(name='spam'))
    assert os.path.isfile('rules/spam.py')
    assert os.path.isfile('featurizers/spam.py')
    assert os.path.isfile('classifiers/spam.py')


def test_startclassifier_creates_yaml_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for d in ['rules', 'featurizers', 'classifiers', 'config']:
        os.makedirs(d, exist_ok=True)
    StartClassifier().execute(FakeArgs(name='spam'))
    assert os.path.isfile('config/spam.yaml')
