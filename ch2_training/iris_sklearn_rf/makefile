ABSOLUTE_PATH := $(shell pwd)
BASE_IMAGE_NAME := cwryu6252/ml-system-design-pattern
TRAINING_PATTERN := training_pattern
TRAINING_PROJECT := iris_sklearn_rf
IMAGE_VERSION := 0.0.1

DOCKERFILE := Dockerfile

.PHONY: dev
dev:
	pip install -r requirements.txt

.PHONY: build
build:
	docker build \
		-t $(BASE_IMAGE_NAME):$(TRAINING_PATTERN)_$(TRAINING_PROJECT)_$(IMAGE_VERSION) \
		-f $(DOCKERFILE) .

.PHONY: train
train:
	mlflow run . --no-conda

.PHONY: ui
ui:
	mlflow ui
