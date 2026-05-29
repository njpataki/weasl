import os
import pytest
from weasl.utils import touch, create_dir_structure


def test_touch_creates_file(tmp_path):
    filepath = str(tmp_path / 'new_file.txt')
    touch(filepath)
    assert os.path.isfile(filepath)


def test_touch_does_not_overwrite_existing(tmp_path):
    filepath = str(tmp_path / 'existing.txt')
    with open(filepath, 'w') as f:
        f.write('original')
    touch(filepath)
    with open(filepath) as f:
        assert f.read() == 'original'


def test_create_dir_structure_makes_directories(tmp_path):
    monkeypatch_chdir = str(tmp_path)
    dirs = [str(tmp_path / 'rules'), str(tmp_path / 'data')]
    create_dir_structure(dirs)
    assert os.path.isdir(str(tmp_path / 'rules'))
    assert os.path.isdir(str(tmp_path / 'data'))


def test_create_dir_structure_touches_files_with_extension(tmp_path):
    paths = [str(tmp_path / 'featurizers' / 'master.py')]
    create_dir_structure(paths)
    assert os.path.isfile(str(tmp_path / 'featurizers' / 'master.py'))


def test_create_dir_structure_idempotent(tmp_path):
    paths = [str(tmp_path / 'rules')]
    create_dir_structure(paths)
    create_dir_structure(paths)  # should not raise
    assert os.path.isdir(str(tmp_path / 'rules'))
