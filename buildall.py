#!/usr/bin/env python

# build a matrix of packages (e.g. multiple python versions) for a
# given architecture and upload them

# usage: buildall.py <recipe>

import sys
from subprocess import check_call, check_output, CalledProcessError
from argparse import ArgumentParser

PYTHON_VERSIONS = ['3.4', '3.5', '3.6']
FAILED = []


def build_and_upload_all(pkg):

    global FAILED
    build_command = ['conda-build', '--dirty']

    print("=" * 70)
    print("BUILDING", pkg, "FOR PYTHON VERSIONS:", PYTHON_VERSIONS)

    for ver in PYTHON_VERSIONS:
        subcommand = ['--python={}'.format(ver), '{}'.format(pkg)]

        try:
            print("*** BUILDING...", pkg, ver)
            ret = check_call(build_command + subcommand)

            print("*** UPLOADING...", pkg, ver)
            output = str(check_output(build_command + ['--output', ]
                                      + subcommand), 'utf8').strip()

            check_call(['anaconda', 'upload', '--user',
                        'cta-observatory', output])

        except CalledProcessError as err:
            FAILED.append('{}:{}:{}'.format(pkg, ver, err))
            print("FAILURE: {}:{}:{}".format(pkg, ver, err))

if __name__ == '__main__':

    par = ArgumentParser(description=('build conda packages for multiple'
                                      ' python versions'))
    par.add_argument('package', type=str, nargs='+',
                     help='package recipe directory')
    args = par.parse_args()

    for package in args.package:
        build_and_upload_all(package)

    if len(FAILED) > 0:
        print("=" * 70)
        print("FAILURES:\n", "\n".join(FAILED))
        sys.stdout.flush()
        sys.exit(1)
