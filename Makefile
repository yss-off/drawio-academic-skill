PYTHON ?= python3

.PHONY: test check check-base package

test:
	$(PYTHON) skill/drawio-academic-skills/evals/smoke_test.py

check:
	$(PYTHON) tools/verify_project.py

check-base:
	$(PYTHON) tools/verify_project.py --with-base

package:
	$(PYTHON) tools/package_skill.py
