from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import sys
sys.path.append('./src')
sys.path.append('./tests')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name = "HatebuCrawler",
    version = "0.1",
    packages = find_packages(exclude=['tests']),
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)