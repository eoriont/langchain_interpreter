# Langchain Interpreter

This project aims to allow for langchain pipelines to be created from a config file.

# To publish

1. Update version number in `pyproject.toml`

2.
        python -m build

3.
        twine upload --skip-existing dist/*
