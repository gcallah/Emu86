#!/bin/sh
#  This file should include all tests run on our assembly emulator.

# exit on any error with that error status:
set -e

export SDIR="selenium_tests"

for s_test_file in $SDIR/*.py; do echo "$s_test_file"; python3 "$s_test_file"; done