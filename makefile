.PHONY: dev
dev:
	pip install pipenv
	PIPENV_VENV_IN_PROJECT=true pipenv shell

.PHONY: dev_sync
dev_sync:
	pipenv sync --dev