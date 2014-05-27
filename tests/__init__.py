#!/usr/bin/env python
import unittest


# Load all test modules - add more here
all_modules = []

from . import test_requests_jwt
all_modules.append(test_requests_jwt)


def suite():
    suite = unittest.TestSuite()

    for mod in all_modules:
        suite.addTests(
                unittest.defaultTestLoader.loadTestsFromModule(mod))

    return suite
