#!/bin/sh
#  This file should include all tests run on our assembly emulator.

# exit on any error with that error status:
set -e

export TDIR="tests"
export ATT_DIR="$TDIR/ATT"
export INTEL_DIR="$TDIR/Intel"
echo "$INTEL_DIR"
$TDIR/test_assemble.py
$TDIR/test_errors.py
$TDIR/test_control_flow.py
$TDIR/test_programs.py
