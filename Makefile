SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate

.PHONY: all clean

all: venv data/alabama_presidential_election.csv data/county_level_percentages.csv

venv: requirements.txt
	test -d venv || python3 -m venv venv
	${ACTIVATE_VENV} && pip install -r requirements.txt
	touch venv

data/alabama_presidential_election.csv: venv
	${ACTIVATE_VENV} && python -m alabama.process.presidential_election_results

data/county_level_percentages.csv: venv
	${ACTIVATE_VENV} && python -m alabama.process.process_election_data

clean:
	rm -rf venv
	find . -name  __pycache__ -exec rm -rf {} \;
