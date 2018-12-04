#!/bin/sh
#  This file should include all tests run on our assembly emulator.

# exit on any error with that error status:
set -e

export JDIR="JavaScript"

for js_test_file in $JDIR/*.py; do echo "$js_test_file"; python3 "$js_test_file"; done