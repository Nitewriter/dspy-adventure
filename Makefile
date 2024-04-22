# Variables
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
SYSTEM_PYTHON = $(or $(shell which python), $(shell which python3))
PYTHON = $(or $(wildcard $(VENV_PYTHON)), $(SYSTEM_PYTHON))

# Virtual environment creation
$(VENV_PYTHON):
	rm -rf $(VENV)
	$(SYSTEM_PYTHON) -m venv $(VENV)

venv: $(VENV_PYTHON)

# Dependency installation
deps: $(VENV_PYTHON) pyproject.toml
	. $(VENV)/bin/activate
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install poetry
	poetry install

clean:
	@deactivate 2>/dev/null || true
	rm -rf $(VENV)

.PHONY: venv deps clean

.DEFAULT_GOAL := deps
