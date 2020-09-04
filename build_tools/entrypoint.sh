#!/usr/bin/env bash
set -e
cd /source
args=$(for name in "${@}"; do echo -n "\"${name}\", "; done)
# Python complains about there being no display. boo hoo.
export PYTHONWARNINGS="ignore"
gimp-console -idf --batch-interpreter python-fu-eval -b "import export_maps;import os;export_maps.main(${args})" -b "pdb.gimp_quit(0)"
