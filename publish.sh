#python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi --config-file ~/.pypirc dist/*
#python3 -m twine upload --repository pypi --config-file ~/.pypirc dist/*