import os
import pytest
from weasl.config import read_config


def test_reads_yaml_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / 'config'
    config_dir.mkdir()
    (config_dir / 'myclassifier.yaml').write_text(
        'rules:\n  - rules.my_rule\nfeatures:\n  - featurizers.my_feat\n'
    )
    cfg = read_config('myclassifier')
    assert cfg['rules'] == ['rules.my_rule']
    assert cfg['features'] == ['featurizers.my_feat']


def test_missing_file_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'config').mkdir()
    with pytest.raises(FileNotFoundError):
        read_config('nonexistent')


def test_empty_yaml_returns_none(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'config').mkdir()
    (tmp_path / 'config' / 'empty.yaml').write_text('')
    cfg = read_config('empty')
    assert cfg is None
