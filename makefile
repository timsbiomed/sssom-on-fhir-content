.DEFAULT_GOAL := all
.PHONY: all build stage deploy-release

TODAY ?=$(shell date +%Y-%m-%d)
VERSION=v$(TODAY)

all: build
build:
	python -m sssom_on_fhir --convert-from-content-dir

stage:
	python -m sssom_on_fhir --stage-release

release/:
	mkdir -p $@

deploy-release: stage | release/
	@test $(VERSION)
	gh release create $(VERSION) --notes "New release." --title "$(VERSION)" release/*
