#!/bin/sh
rm -r htmlcov
coverage3 erase
coverage3 run --source=contextshell -m unittest discover -s tests -t tests -p '*Tests.py'
coverage3 report html && firefox htmlcov/index.html
