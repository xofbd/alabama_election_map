SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate

.PHONY: all clean deploy-dev deploy-prod deploy-standalone tests

all: clean data/*_election_results.csv deploy-dev

# Creating CSV files
data/%_results.csv: .process alabama/process/%.py
	${ACTIVATE_VENV} && python -m alabama.process.$*

# Deployment
deploy-dev: .deploy
	${ACTIVATE_VENV} && bin/deploy dev

deploy-prod: .deploy
	${ACTIVATE_VENV} && bin/deploy prod

deploy-standalone: .deploy
	${ACTIVATE_VENV} && bin/deploy standalone

# Virtual Environment
venv:
	python3 -m venv venv

.pip-tools: venv requirements/pip-tools.txt
	${ACTIVATE_VENV} && pip install -r requirements/pip-tools.txt
	touch .pip-tools

.process: .pip-tools requirements/base.txt requirements/requirements-process.txt
	${ACTIVATE_VENV} && pip-sync $(word 2, $^) $(word 3, $^)
	rm -f .deploy .test
	touch .process

.deploy: .pip-tools requirements/base.txt requirements/requirements-deploy.txt
	${ACTIVATE_VENV} && pip-sync $(word 2, $^) $(word 3, $^)
	rm -f .process .test
	touch .deploy

.test: .pip-tools requirements/base.txt requirements/requirements-deploy.txt requirements/test.txt
	${ACTIVATE_VENV} && pip-sync $(word 2, $^) $(word 3, $^) $(word 4, $^)
	rm -rf .proces .deploy
	touch .test

# Creating requirement files
requirements/base.txt: .pip-tools
	${ACTIVATE_VENV} && pip-compile requirements/base.in

requirements/requirements-%.txt: requirements/base.txt requirements/requirements-%.in
	${ACTIVATE_VENV} && pip-compile requirements/requirements-$*.in

requirements/test.txt: requirements/requirements-deploy.txt requirements/test.in
	${ACTIVATE_VENV} && pip-compile requirements/test.in

requirements.txt: .deploy
	${ACTIVATE_VENV} && pip freeze > requirements.txt

# Utility
tests: .test
	${ACTIVATE_VENV} && pytest -v tests

clean:
	rm -f .pip-tools .process .deploy .test
	rm -rf venv
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf
