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

