#!/bin/env python

# build a matrix of packages (e.g. multiple python versions) for a
# given architecture and upload them

# usage: buildall.py <recipe>

import sys
from subprocess import check_call, check_output, CalledProcessError

PYTHON_VERSIONS = ['3.4', '3.5']


def build_and_upload_all(pkg):

    failed = []
    build_command = ['conda-build', '--dirty']

    print("BUILDING", pkg, "FOR PYTHON VERSIONS:", PYTHON_VERSIONS)

    for ver in PYTHON_VERSIONS:
        subcommand = ['--python={}'.format(ver), '{}'.format(pkg)]

        try:
            print("*** BUILDING...", pkg, ver)
            ret = check_call(build_command + subcommand)

            print("*** UPLOADING...", pkg, ver)
            output = check_output(build_command + ['--output', ] + subcommand)
            check_call(['anaconda', 'upload', '--user',
                        'cta-observatory', output])

        except CalledProcessError as err:
            failed.append('{}:{}:{}'.format(pkg, ver, err))

    if len(failed) > 0:
        print("FAILED PACKAGES:\n", "\n".join(failed))


if __name__ == '__main__':

    build_and_upload_all(sys.argv[1])
