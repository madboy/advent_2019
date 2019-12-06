.PHONY: test all

DAYS=`ls -l src/*.py | grep -v init | wc -l`

test:
	pytest src/*.py

all:
	seq 1  $(DAYS) | xargs -I % ./advent.py %
