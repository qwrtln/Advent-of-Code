#!/usr/bin/env bash

FILE=$1

hyperfine --warmup 3 "python $FILE.py"
hyperfine --warmup 3 "pypy3 $FILE.py"
