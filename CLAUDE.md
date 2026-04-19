# CLAUDE.md

## What this project is

weasl is a CLI framework for weakly supervised machine learning. Users scaffold a project, write heuristic labeling rules and feature extractors, then train classifiers on the noisy labels those rules produce. Think of it as lightweight Snorkel.

## Commands

```bash
# run the test suite (always do this before committing)
python -m pytest

# install for development
pip install -e ".[dev]"

# CLI entry point
weasl --help
```

## Repository layout

```
weasl/          core package
  main.py       CLI entry point (argparse, routes to commands)
  commands.py   startproject / startclassifier / train implementations
  rules.py      Rule base class + RegexInFieldsRule
  features.py   call_and_concat — runs feature funcs and merges results
  config.py     read_config — loads a classifier's YAML config
  project_env.py  dynamic import of user rules/features/classifiers
  regex.py      punctuation-aware regex match (string or array input)
  utils.py      touch, create_dir_structure filesystem helpers
tests/          pytest suite, one file per module
```

## Key architectural decisions

- **Plugin system via dynamic import.** User code (rules, features, classifiers) lives in flat `.py` files inside `rules/`, `featurizers/`, `classifiers/`. `project_env.py` imports them at runtime by appending `cwd` to `sys.path`. No registration or decorators needed.
- **Config-driven wiring.** `config/<name>.yaml` lists which rules, features, and classifiers to use for a given classifier by dotted name (`module.symbol`).
- **Rule interface.** Rules are callables: `(DataFrame) -> Series`. `RegexInFieldsRule` is the only built-in implementation; users subclass `Rule` or write plain functions.
- **Feature interface.** Feature functions take a `DataFrame` and return a `DataFrame`. Column names get auto-prefixed with `module.function.column` for traceability.

## What is not implemented yet

- Evaluation / metrics (no predict, score, or confusion matrix)
- Rule types beyond regex (keyword lists, model-based rules, etc.)
- Multi-rule label aggregation (currently each rule trains a separate model)
- CLI output / progress logging
- The `master.yaml` config path is deprecated but still created by `startproject` (TODO in commands.py:39)

## Development conventions

- Branch: work on `claude/review-old-repo-GSf1x` (or a new feature branch off it), never push directly to `main`
- Tests: add a test for every behavioral change; run `pytest` before committing
- No docstrings or inline comments unless the reason is non-obvious
- Prefer editing existing files over adding new ones
