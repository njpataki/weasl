# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.0] - 2026-04-19

### Added
- Full test suite: 35 tests across all modules (`regex`, `rules`, `features`, `config`, `utils`, `commands`, `project_env`)
- `pyproject.toml` replacing legacy `setup.py` packaging
- `pytest` as an optional dev dependency

### Fixed
- Python 3 compatibility: replaced all `dict.iteritems()` with `.items()`
- `pickle.dump` now opens files in binary mode (`'wb'`) as required by Python 3
- Missing `return` statement in `regex.regex_search` for array inputs (previously silently returned `None`)
- `yaml.load()` replaced with `yaml.safe_load()` to fix deprecation warning and security issue
- `PyYAML` added to install dependencies (was imported but not declared)

## [0.1.0] - 2017-07-16

### Added
- `weasl startproject` command to scaffold a project directory structure
- `weasl startclassifier` command to scaffold per-classifier stubs
- `weasl train` command to run a full weak supervision pipeline
- `RegexInFieldsRule` for pattern-based weak label generation
- Dynamic module loading for user-defined rules, features, and classifiers
- YAML-based classifier configuration
