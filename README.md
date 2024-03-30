# Packaging your python code with project.toml

## reference:

https://www.youtube.com/watch?v=v6tALyc4C10

## commands:

```bash
# create env to test package
python -m venv venv
# activate venv
. venv/Scripts/activate

# install in editable mode
pip install -e .

# fix vscode pylance cannot resolve package in editable mode
# https://stackoverflow.com/a/76897706
pip install -e . --config-settings editable_mode=strict

# uninstall 
pip uninstall snakesay

# run module using __main__.py
python -m normalize
python -m gitfiles

# run script defined in pyproject.toml
snakey

# deactivate venv
deactivate
```

