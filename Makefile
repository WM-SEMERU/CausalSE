.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard nbs/*.ipynb)

<<<<<<< HEAD
all: icodegen docs

icodegen: $(SRC)
	nbdev_build_lib
	touch icodegen
=======
all: mlproj_template docs

mlproj_template: $(SRC)
	nbdev_build_lib
	touch mlproj_template
>>>>>>> 4140f24734dc43a0cec843110b40849f867f6944

sync:
	nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_conda_package
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist