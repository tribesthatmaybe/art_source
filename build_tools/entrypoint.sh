#!/usr/bin/env bash
set -e
set -x
cd /source
# Python complains about there being no display. boo hoo.
export PYTHONWARNINGS="ignore"
echo "import export_maps;export_maps.entrypoint($@)"
gimp-console -idf --batch-interpreter python-fu-eval -b "import export_maps; export_maps.entrypoint('$*')" -b "pdb.gimp_quit(0)"
