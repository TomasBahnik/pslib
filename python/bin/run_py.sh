#!/bin/bash
PYTHONPATH=$(pwd)
export PYTHONPATH
echo "PYTHONPATH = $PYTHONPATH"
echo "running python $@"
python "$@"
