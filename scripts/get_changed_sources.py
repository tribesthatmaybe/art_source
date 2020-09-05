#!/usr/bin/env python3
"""
Currently only does textures cos that's what I'm playing with now
"""

import argparse
import json
import os
import subprocess
import yaml

SHA_ENV = 'GITHUB_SHA'

EXT_HELP = ('extensions to get (may specify more than one). if not specified, '
            + 'all changed files will be returned')

OUT_HELP = ('If you wish to output to a file instead of stdout, specify the '
            + 'file with this flag')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('sha', nargs='?',
                        default=os.environ.get(SHA_ENV))
    parser.add_argument('--json', action='store_true', help='Output in json')
    parser.add_argument('--yaml', action='store_true', help='Output in yaml')
    parser.add_argument('--ext', nargs='*', help=EXT_HELP)
    # Short help for below: Build from changed Metadata
    parser.add_argument('--meta', action='store_true',
                        help='get assets [of type[s] `--ext`, if provided] whose sidecars have changed.')
    parser.add_argument('--only_meta', action='store_true',
                        help='only build assets whose metadata has been updated.')
    parser.add_argument('--out', help=OUT_HELP)

    parsed_args = parser.parse_args()

    if parsed_args.meta:
        raise NotImplementedError()

    sha = parsed_args.sha

    if sha is None:
        # ToDo get from latest git commit
        # ToDo also allow for env var or something to get changed wc files
        raise NotImplementedError(
            'Must have env var {} set, '.format(SHA_ENV)
            + 'or pass in the sha for a commit as an argument'
        )

    cmd = ['git', 'log', '-1', '--name-only', '--no-notes', u'--pretty=format:', sha]
    res = subprocess.check_output(cmd, cwd=os.getcwd()).decode()
    files = [f.strip() for f in res.splitlines()]

    if parsed_args.json:
        # json _is_ yaml, technically
        print(json.dumps(files, indent=4))
    elif parsed_args.yaml:
        print(yaml.dumps(files, indent=4))
    else:
        print('\n'.join(files))


if __name__ == '__main__':
    main()
