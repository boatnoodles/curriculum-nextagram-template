# https://github.com/coleifer/flask-peewee/blob/master/runtests.py
import os
import sys
import unittest

import tests


def run_tests(*test_args):
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.failures:
        sys.exit(1)
    elif result.errors:
        sys.exit(2)
    sys.exit(0)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
