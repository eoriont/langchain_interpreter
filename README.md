# Langchain Interpreter

[![Documentation Status](https://readthedocs.org/projects/langchain-interpreter/badge/?version=latest)](https://langchain-interpreter.readthedocs.io/en/latest/?badge=latest)

This project aims to allow for langchain pipelines to be created from a config file.

Documentation: https://langchain-interpreter.readthedocs.io/

## To publish

1. Update version number in `pyproject.toml`

2.
```
python -m build
```

3.
```
twine upload --skip-existing dist/*
```

## Documentation

This command generates docs for each module? (run in project dir)

```
sphinx-apidoc -f -o docs src/langchain_interpreter/
```

This command builds the docs:
```
cd docs
make html
```

This command cleans the html out:
```
cd docs
make clean
```

## For examples

Install the project:
```
pip install -e .
```
