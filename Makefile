.PHONY: docs
init:
	pip install -e .[socks]
	pip install -r requirements-dev.txt
ci:
	pytest --cov-report=xml --cov-config=.coveragerc --cov=badger_voter_sdk/
