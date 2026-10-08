#!/bin/bash
# Runs the seven steps, then the checks. About 2 minutes on a laptop; nothing to install.
set -e
cd "$(dirname "$0")"
for step in step1_recall step2_energy step3_cut step4_ghosts step5_capacity step6_dense step7_attention; do
  echo
  echo "=== $step.py"
  python3 $step.py
done
echo
python3 tests.py
