SHELL = /bin/bash
ACTIVATE_VENV = source venv/bin/activate

outputs = .pip-tools .process .deploy .test
csvs = $(wildcard data/*_election_results.csv)
reqs = $(wildcard requirements/*.txt) requirements.txt

.PHONY: all
all: clean $(csvs) deploy-dev

# Creating CSV files
data/%_results.csv: alabama/process/%.py | .process
	$(ACTIVATE_VENV) && python -m alabama.process.$*

# Deployment
.PHONY: deploy-dev deploy-prod deploy-standalone
deploy-dev deploy-prod deploy-standalone: | .deploy
	$(ACTIVATE_VENV) && bin/deploy $(subst deploy-,,$@)

# Virtual environments
venv:
	python3 -m venv $@

.pip-tools: requirements/pip-tools.txt | venv
	$(ACTIVATE_VENV) && pip install -r $<
	touch $@

.process: requirements/base.txt requirements/process.txt | .pip-tools
	$(ACTIVATE_VENV) && pip-sync $^
	rm -f $(filter-out $@ .pip-tools, $(outputs))
	touch $@

.deploy: requirements/base.txt requirements/deploy.txt | .pip-tools
	$(ACTIVATE_VENV) && pip-sync $^
	rm -f $(filter-out $@ .pip-tools, $(outputs))
	touch $@

.test: requirements/base.txt requirements/deploy.txt requirements/test.txt | .pip-tools
	$(ACTIVATE_VENV) && pip-sync $^
	rm -f $(filter-out $@ .pip-tools, $(outputs))
	touch $@

# Creating requirement files
.PHONY: requirements
requirements: $(reqs)

requirements/%.txt: requirements/%.in requirements/constraints.txt | .pip-tools
	$(ACTIVATE_VENV) && pip-compile $<

requirements/pip-tools.txt:
# Avoids circular reference
	:

requirements/deploy.txt: requirements/base.txt

requirements/process.txt: requirements/base.txt

requirements/test.txt: requirements/deploy.txt

requirements.txt: requirements/deploy.txt | .deploy
	$(ACTIVATE_VENV) && pip freeze > $@

# Utility
.PHONY: clean tests

tests: .test
	$(ACTIVATE_VENV) && pytest -s tests

clean:
	rm -f $(outputs)
	rm -rf venv
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf
