VERSION ?= $(shell cat VERSION)

# unittest > bump > deploy 


.PHONY: help setup  setupdev unittest clean
.DEFAULT_GOAL := help


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: venv/touchfile ## install dependencies

venv/touchfile: inspectphoto/requirements.txt ## install a virtual env and app requirements
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur inspectphoto/requirements.txt
	touch venv/touchfile

setupdev: venv/touchfile.dev ## install dev dependencies

venv/touchfile.dev: inspectphoto/requirements-dev.txt ## install dev dependencies
	. venv/bin/activate; pip install -Ur inspectphoto/requirements-dev.txt
	touch venv/touchfile.dev

test:  ## run all component tests
	@start=$$(date +%s); \
    echo $@ start: $$start > test.log 	
	- make lint; echo "lint:" [$$?] $$(date +%s) >> test.log
	- make unittest; echo "unittest:" [$$?] $$(date +%s) >> test.log
	- make coverage; echo "coverage:" [$$?] $$(date +%s)  >> test.log
	@end=$$(date +%s); \
    echo $@ stop: $$end >> test.log
	cat test.log

docs: setupdev ## create/update documentation
	@echo "==== $@ ===="
	. venv/bin/activate; export PYTHONPATH='./inspectphoto'; python -m pdoc inspectphoto -o docs/generated

unittest: setup setupdev ## run unitest
	@echo "==== $@ ===="
	. venv/bin/activate; cd inspectphoto; python -m pytest -rA ..

demo: setup ## run from source
	. venv/bin/activate; python inspectphoto/inspectphoto.py -i inspectphoto/static/img/jester.jpg
	
run: setup ## run from source
	. venv/bin/activate; python inspectphoto/main.py

build: setup Dockerfile ## build docker image
	docker build -t inspectphoto .

docker: build ## run dockerize image (read from stdin)
	docker run -p 5000:5000 -i inspectphoto

package: setup ## create a python package under dist folder
	. venv/bin/activate; python setup.py sdist

tar: setup ## create a tar package (needs GIT repo)
	git archive --format=tar.gz -o inspectphoto.tar.gz HEAD -v 

deploy: ## Deploy to deta (needs deta login)
	cd inspectphoto; ~/.deta/bin/deta deploy

clean:
	# clean up
	rm -rf venv

