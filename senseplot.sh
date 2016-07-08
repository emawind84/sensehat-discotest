#!/usr/bin/env bash

SCRIPT_BASE_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SCRIPT_NAME="${0##*/}"

export PATH=/home/pi/python_example/ipython/bin:$PATH

set -e

echo "Base path: $SCRIPT_BASE_PATH"
echo "Script name: $SCRIPT_NAME"

cd $SCRIPT_BASE_PATH

python senseplot.py $1