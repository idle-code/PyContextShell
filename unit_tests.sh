#!/bin/bash

export PYTHONPATH=`pwd`

coverage run \
	--branch \
	--source ./contextshell \
	-m unittest \
		discover \
		--pattern '*Tests.py' \
		--top-level-directory ./ \
		--start-directory ./tests/unit/ \
		./tests/unit/
TESTS_PASSED=$?

if [[ $TESTS_PASSED -eq 0 ]];
then
	coverage report -m
fi
