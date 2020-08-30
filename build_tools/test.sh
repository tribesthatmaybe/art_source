set -e
#!/usr/bin/env bash
cp /source/build_tools/export_maps.py /usr/lib64/python2.7/site-packages/

# to get path
#gimp-console -idf --batch-interpreter python-fu-eval -b "import sys;print('\n'.join(sys.path))" -b "pdb.gimp_quit(1)"

gimp-console -idf --batch-interpreter python-fu-eval -b "import export_maps;import os;print(export_maps.process(os.getcwd()))" -b "pdb.gimp_quit(0)"
