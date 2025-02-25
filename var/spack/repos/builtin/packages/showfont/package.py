# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Showfont(AutotoolsPackage, XorgPackage):
    """showfont displays data about a font from an X font server.
    The information shown includes font information, font properties,
    character metrics, and character bitmaps."""

    homepage = "https://cgit.freedesktop.org/xorg/app/showfont"
    xorg_mirror_path = "app/showfont-1.0.5.tar.gz"

    version('1.0.5', sha256='566e34a145ea73397724d46e84f6a9b3691cf55d0fcb96ec7f917b2b39265ebb')

    depends_on('libfs')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
