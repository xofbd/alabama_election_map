SHELL = /bin/bash
ACTIVATE_VENV = source venv/bin/activate
OUTPUTS = .pip-tools .process .deploy .test
CSV = $(wildcard data/*_election_results.csv)
REQ = $(wildcard requirements/*.txt) requirements.txt
SRC = $(filter-out .pip-tools, $^)

.PHONY: all
all: clean $(CSV) deploy-dev

# Creating CSV files
data/%_results.csv: .process alabama/process/%.py
	$(ACTIVATE_VENV) && python -m alabama.process.$*

# Deployment
.PHONY: deploy-dev deploy-prod deploy-standalone
deploy-dev deploy-prod deploy-standalone: .deploy
	$(ACTIVATE_VENV) && bin/deploy $(subst deploy-,,$@)

# Virtual environments
venv:
	python3 -m venv $@

.pip-tools: requirements/pip-tools.txt venv 
	$(ACTIVATE_VENV) && pip install -r $<
	touch $@

.process: .pip-tools requirements/base.txt requirements/process.txt
	$(ACTIVATE_VENV) && pip-sync $(SRC)
	rm -f $(filter-out $@ .pip-tools, $(OUTPUTS))
	touch $@

.deploy: .pip-tools requirements/base.txt requirements/deploy.txt
	$(ACTIVATE_VENV) && pip-sync $(SRC)
	rm -f $(filter-out $@ .pip-tools, $(OUTPUTS))
	touch $@

.test: .pip-tools requirements/base.txt requirements/deploy.txt requirements/test.txt
	$(ACTIVATE_VENV) && pip-sync $(SRC)
	rm -f $(filter-out $@ .pip-tools, $(OUTPUTS))
	touch $@

# Creating requirement files
.PHONY: requirements
requirements: $(REQ)

requirements/%.txt: .pip-tools requirements/%.in
	$(ACTIVATE_VENV) && pip-compile $(word 2, $^)

requirements/pip-tools.txt:
	 # Avoids circular reference

requirements/deploy.txt: requirements/base.txt

requirements/process.txt: requirements/base.txt

requirements/test.txt: requirements/deploy.txt

requirements.txt: .deploy
	$(ACTIVATE_VENV) && pip freeze > $@

# Utility
.PHONY: clean tests

tests: .test
	$(ACTIVATE_VENV) && pytest -s tests

clean:
	rm -f $(OUTPUTS)
	rm -rf venv
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf
