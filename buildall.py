#!/usr/bin/env python

# build a matrix of packages (e.g. multiple python versions) for a
# given architecture and upload them

# usage: buildall.py <recipe>

import sys
from subprocess import check_call, check_output, CalledProcessError
from argparse import ArgumentParser

PYTHON_VERSIONS = ['3.4', '3.5', '3.6']
FAILED = []


def build_and_upload_all(pkg, user):

    global FAILED
    build_command = ['conda-build', '--dirty', '-c cta-observatory']

    print("=" * 70)
    print("BUILDING", pkg, "FOR PYTHON VERSIONS:", PYTHON_VERSIONS)

    for ver in PYTHON_VERSIONS:
        subcommand = ['--python={}'.format(ver), '{}'.format(pkg)]

        try:
            print("*** BUILDING...", pkg, ver)
            ret = check_call(build_command + subcommand)

            print("*** FIND PACKAGE...", pkg, ver)
            output = str(check_output(build_command + ['--output', ]
                                      + subcommand), 'utf8').strip()
            print("*** UPLOADING <{}>".format(output))
            check_call(['anaconda', 'upload', '--user', user, output])

        except CalledProcessError as err:
            FAILED.append('{}:{}:{}'.format(pkg, ver, err))
            print("FAILURE: {}:{}:{}".format(pkg, ver, err))

if __name__ == '__main__':

    par = ArgumentParser(description=('build conda packages for multiple'
                                      ' python versions'))
    par.add_argument('package', type=str, nargs='+',
                     help='package recipe directory')
    par.add_argument('--user', type=str, help='username on Anaconda Cloud',
                     default='cta-observatory')
    args = par.parse_args()

    for package in args.package:
        build_and_upload_all(package, user=args.user)

    if len(FAILED) > 0:
        print("=" * 70)
        print("FAILURES:\n\n", "\n".join(FAILED))
        sys.stdout.flush()
        sys.exit(1)
