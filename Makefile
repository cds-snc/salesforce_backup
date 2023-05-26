.PHONY: requirements requirements-dev clean test postCreateCommand

# Default command runs the requirements and requriements-dev targets
default: clean requirements requirements-dev

run-local:
	python main.py

# Used by the devcontainer, you shouldn't have to run this
postCreateCommand:
	@echo "Run 'make' to install requirements and 'make test' to run tests"
	@sudo apt-get update && apt-get install -y --no-install-recommends \
		tmux	\
		vim

# Install requirements
requirements:
	pip install -r requirements.txt

# Install dev requirements
requirements-dev:
	pip install -r requirements-dev.txt

test:
	pytest .

fmt:
	black .
	terraform fmt -recursive

fmt-ci:
	black . --check

clean:
	@rm -rf csv
	@rm -rf failed