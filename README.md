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
# https://stackoverflow.com/a/76301809
pip install -e . --config-settings editable_mode=compat
vscode: ctrl+shift+p, "Python: Restart language server"

# uninstall 
pip uninstall atrox3d

# run module using __main__.py
python -m normalize
python -m gitfiles
python -m simplegit

# run script defined in pyproject.toml
normalize
gitfiles
simplegit

# deactivate venv
deactivate
```

