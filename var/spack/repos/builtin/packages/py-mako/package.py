# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMako(PythonPackage):
    """A super-fast templating language that borrows the best
       ideas from the existing templating languages."""

    homepage = "https://www.makotemplates.org/"
    pypi = "Mako/Mako-1.0.1.tar.gz"
    git = "https://github.com/sqlalchemy/mako"

    version('1.1.6', sha256='4e9e345a41924a954251b95b4b28e14a301145b544901332e658907a7464b6b2')
    version('1.1.5', sha256='169fa52af22a91900d852e937400e79f535496191c63712e3b9fda5a9bed6fc3')
    version('1.1.4', sha256='17831f0b7087c313c0ffae2bcbbd3c1d5ba9eeac9c38f2eb7b50e8c99fe9d5ab')
    version('1.0.4', sha256='fed99dbe4d0ddb27a33ee4910d8708aca9ef1fe854e668387a9ab9a90cbf9059')
    version('1.0.1', sha256='45f0869febea59dab7efd256fb451c377cbb7947bef386ff0bb44627c31a8d1c')

    depends_on('python@2.7:2,3.4:', when='@1.1.0:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-markupsafe@0.9.2:', type=('build', 'run'))
