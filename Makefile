SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate

.PHONY: all clean deploy-dev deploy-prod

all: clean data/*_election_results.csv deploy-dev

# Creating CSV files
data/%_results.csv: .process alabama/process/%.py
	${ACTIVATE_VENV} && python -m alabama.process.$*

# Deployment
deploy-dev: .deploy
	${ACTIVATE_VENV} && bin/deploy dev

deploy-prod: .deploy
	${ACTIVATE_VENV} && bin/deploy prod

# Virtual Environment
venv:
	python3 -m venv venv

.pip-tools: venv requirements/pip-tools.txt
	${ACTIVATE_VENV} && pip install -r requirements/pip-tools.txt
	touch .pip-tools

.process: .pip-tools requirements/base.txt requirements/requirements-process.txt
	${ACTIVATE_VENV} && pip-sync $(word 2, $^) $(word 3, $^)
	rm -f .deploy
	touch .process

.deploy: .pip-tools requirements/base.txt requirements/requirements-deploy.txt
	${ACTIVATE_VENV} && pip-sync $(word 2, $^) $(word 3, $^)
	rm -f .process
	touch .deploy

# Creating requirement files
requirements/base.txt: .pip-tools
	${ACTIVATE_VENV} && pip-compile requirements/base.in

requirements/requirements-%.txt: requirements/base.txt requirements/requirements-%.in
	${ACTIVATE_VENV} && pip-compile requirements/requirements-$*.in

requirements.txt: .deploy
	${ACTIVATE_VENV} && pip freeze > requirements.txt

# Utility
clean:
	rm -f .pip-tools .process .deploy
	rm -rf venv
	find . | grep __pycache__ | xargs rm -rf
