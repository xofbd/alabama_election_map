SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate

.PHONY: all clean

all: venv

venv: requirements.txt
	test -d venv || python3 -m venv venv
	${ACTIVATE_VENV} && pip install -r requirements.txt
	touch venv

clean:
	rm -rf venv
	find . -name  __pycache__ -exec rm -rf {} \;
