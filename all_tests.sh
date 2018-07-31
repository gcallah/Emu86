#!/bin/sh
#  This file should include all tests run on our assembly emulator.

# exit on any error with that error status:
set -e

export TDIR="tests"
export ATT_DIR="$TDIR/ATT"
export INTEL_DIR="$TDIR/Intel"
export MIPS_DIR="$TDIR/MIPS"

$INTEL_DIR/test_assemble.py
$INTEL_DIR/test_errors.py
$INTEL_DIR/test_control_flow.py
$INTEL_DIR/test_programs.py

$ATT_DIR/test_assemble.py
$ATT_DIR/test_errors.py
$ATT_DIR/test_control_flow.py
$ATT_DIR/test_programs.py

$MIPS_DIR/test_assemble.py
$MIPS_DIR/test_errors.py
$MIPS_DIR/test_programs.py