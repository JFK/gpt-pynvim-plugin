.PHONY: clean build upload

clean:
	rm -rf dist
	rm -rf build
	rm -rf gpt_pynvim.egg-info

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*
