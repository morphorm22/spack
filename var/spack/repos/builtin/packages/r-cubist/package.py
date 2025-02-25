# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCubist(RPackage):
    """Rule- And Instance-Based Regression Modeling.

    Regression modeling using rules with added instance-based corrections."""

    cran = "Cubist"

    version('0.3.0', sha256='88a76e7f858a8e978a73a97ce6a3504201d889517b39ce862cef734dcf9eb263')
    version('0.2.3', sha256='19845f585e073f316bb4bdf74b28a624e839561faeedd40ef5548960c5b1e1f4')
    version('0.2.2', sha256='cd3e152cc72ab33f720a8fb6b8b6787171e1c037cfda48f1735ab692ed6d85d4')
    version('0.2.1', sha256='b310c3f166f15fa3e16f8d110d39931b0bb1b0aa8d0c9ac2af5a9a45081588a3')
    version('0.0.19', sha256='101379979acb12a58bcf32a912fef32d497b00263ebea918f2b85a2c32934aae')

    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
