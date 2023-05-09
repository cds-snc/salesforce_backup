.PHONY: requirements requirements-dev clean test

# Default command runs the requirements and requriements-dev targets
default: clean requirements requirements-dev

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

clean:
	@rm -rf csv
	@rm -rf failed