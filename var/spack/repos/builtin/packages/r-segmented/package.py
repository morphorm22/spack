# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSegmented(RPackage):
    """Regression Models with Break-Points / Change-Points Estimation.

    Given a regression model, segmented 'updates' it by adding one or more
    segmented (i.e., piece-wise linear) relationships. Several variables with
    multiple breakpoints are allowed. The estimation method is discussed in
    Muggeo (2003, <doi:10.1002/sim.1545>) and illustrated in Muggeo (2008,
    <https://www.r-project.org/doc/Rnews/Rnews_2008-1.pdf>). An approach for
    hypothesis testing is presented in Muggeo (2016,
    <doi:10.1080/00949655.2016.1149855>), and interval estimation for the
    breakpoint is discussed in Muggeo (2017, <doi:10.1111/anzs.12200>)."""

    cran = "segmented"

    version('1.4-0', sha256='306940d3fe38588d5f52a52a217b560620b9ec9f338b32f604dfd78ffd43c276')
    version('1.3-4', sha256='8276bfbb3e5c1d7a9a61098f72ac9b2b0f52c89ae9f9b715f76b22303cc3902d')
    version('1.3-1', sha256='b9b6e82bf72f108c69cb8fa01bd02fb99946c73ca3c8c2f8ae0abb1f460c143d')
    version('1.0-0', sha256='eeadc89b4bb4744bbd1e4e6c3b6536ff96fc7ee09016228dfdc0a8ebdc74fac5')
    version('0.5-4.0', sha256='7ff63a19915cbd1e190d3a4875892b4c7bd97890b0dc2909126348a19aec4071')
    version('0.5-2.2', sha256='3aa7136370dd77911ba8e061b5215560d120bc71f355eeadc0856389dfecb2f1')
    version('0.5-1.4', sha256='b1dc5f79ccc076c2943b15fe4f339368afa241797b7e80c91b62132cfa66809c')

    depends_on('r-mass', type=('build', 'run'), when='@1.4-0:')
