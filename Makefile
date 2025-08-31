PY=python3
VENV=.venv

.PHONY: venv install run dev fmt lint clean

venv:
	$(PY) -m venv $(VENV)
	. $(VENV)/bin/activate; pip install -U pip

install:
	. $(VENV)/bin/activate; pip install -r requirements.txt

run:
	. $(VENV)/bin/activate; uvicorn app.main:app --reload

dev:
	. $(VENV)/bin/activate; fastapi dev app/main.py

clean:
	rm -rf $(VENV) students.db __pycache__ .pytest_cache .mypy_cache

