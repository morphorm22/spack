"""
Test for multi_method dispatch.
"""
import unittest

import spack.packages as packages
from spack.multimethod import *
from spack.version import *
from spack.spec import Spec
from spack.multimethod import when
from spack.test.mock_packages_test import *


class MultiMethodTest(MockPackagesTest):

    def test_no_version_match(self):
        pkg = packages.get('multimethod@2.0')
        self.assertRaises(NoSuchMethodError, pkg.no_version_2)


    def test_one_version_match(self):
        pkg = packages.get('multimethod@1.0')
        self.assertEqual(pkg.no_version_2(), 1)

        pkg = packages.get('multimethod@3.0')
        self.assertEqual(pkg.no_version_2(), 3)

        pkg = packages.get('multimethod@4.0')
        self.assertEqual(pkg.no_version_2(), 4)


    def test_version_overlap(self):
        pkg = packages.get('multimethod@2.0')
        self.assertEqual(pkg.version_overlap(), 1)

        pkg = packages.get('multimethod@5.0')
        self.assertEqual(pkg.version_overlap(), 2)


    def test_mpi_version(self):
        pkg = packages.get('multimethod^mpich@3.0.4')
        self.assertEqual(pkg.mpi_version(), 3)

        pkg = packages.get('multimethod^mpich2@1.2')
        self.assertEqual(pkg.mpi_version(), 2)

        pkg = packages.get('multimethod^mpich@1.0')
        self.assertEqual(pkg.mpi_version(), 1)


    def test_undefined_mpi_version(self):
        # This currently fails because provides() doesn't do
        # the right thing undefined version ranges.
        # TODO: fix this.
        pkg = packages.get('multimethod^mpich@0.4')
        self.assertEqual(pkg.mpi_version(), 0)


    def test_default_works(self):
        pkg = packages.get('multimethod%gcc')
        self.assertEqual(pkg.has_a_default(), 'gcc')

        pkg = packages.get('multimethod%intel')
        self.assertEqual(pkg.has_a_default(), 'intel')

        pkg = packages.get('multimethod%pgi')
        self.assertEqual(pkg.has_a_default(), 'default')


    def test_architecture_match(self):
        pkg = packages.get('multimethod=x86_64')
        self.assertEqual(pkg.different_by_architecture(), 'x86_64')

        pkg = packages.get('multimethod=ppc64')
        self.assertEqual(pkg.different_by_architecture(), 'ppc64')

        pkg = packages.get('multimethod=ppc32')
        self.assertEqual(pkg.different_by_architecture(), 'ppc32')

        pkg = packages.get('multimethod=arm64')
        self.assertEqual(pkg.different_by_architecture(), 'arm64')

        pkg = packages.get('multimethod=macos')
        self.assertRaises(NoSuchMethodError, pkg.different_by_architecture)


    def test_dependency_match(self):
        pkg = packages.get('multimethod^zmpi')
        self.assertEqual(pkg.different_by_dep(), 'zmpi')

        pkg = packages.get('multimethod^mpich')
        self.assertEqual(pkg.different_by_dep(), 'mpich')

        # If we try to switch on some entirely different dep, it's ambiguous,
        # but should take the first option
        pkg = packages.get('multimethod^foobar')
        self.assertEqual(pkg.different_by_dep(), 'mpich')


    def test_virtual_dep_match(self):
        pkg = packages.get('multimethod^mpich2')
        self.assertEqual(pkg.different_by_virtual_dep(), 2)

        pkg = packages.get('multimethod^mpich@1.0')
        self.assertEqual(pkg.different_by_virtual_dep(), 1)
