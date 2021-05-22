rem Install all dependencies:
pip3 install -r requirements.txt
pip3 install poetry
poetry lock
poetry install

rem Install pre-commit hooks:
pre-commit install
