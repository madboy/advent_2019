.PHONY: test all

test:
	pytest src/*.py

all:
	seq 1 6 | xargs -I % ./advent.py %
