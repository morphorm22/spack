# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spral(AutotoolsPackage, CudaPackage):
    """SPRAL: The Sparse Parallel Robust Algorithm Library"""

    homepage = "https://www.numerical.rl.ac.uk/spral"
    url      = "https://github.com/ralna/spral/archive/refs/tags/v2016.09.23.tar.gz"

    version('2016.09.23', sha256='7eb0919c2c03af8811610ac50f8d7126d6193aad71eef1928c17a28b26a6acbe')
    version('2015.04.20', sha256='2deef764ef9c7c8553060f3204dab8af87c7cf62499ea1bd2bba43041af1e967')

    variant('blas', default=True,
            description="Build with BLAS")
    variant('lapack', default=True,
            description="Build with Lapack")
    variant('metis',   default=False,
            description="Build with METIS partitioning support")
    variant('debug',   default=False,
            description="Build with debug flags")

    depends_on("blas",         when='+blas')
    depends_on("netlib-lapack",       when='+lapack')
    depends_on("metis",        when='+metis')
    depends_on("cuda",         when='+cuda')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # SPRAL does not build correctly in parallel
    parallel = False

    def setup_build_environment(self, env):
        cuda_arch = self.spec.variants['cuda_arch'].value[0]
        env.set('NVCCFLAGS', '-arch=sm_%s' % cuda_arch)

    def configure_args(self):
        spec = self.spec

        args = ["--prefix=%s" % self.prefix]

        if 'blas' in spec:
            # blas_dir = spec['blas'].prefix
            blas_lib = spec['blas'].libs.ld_flags
            args.extend(["--with-blas=%s" % blas_lib])

        if 'lapack' in spec:
            # lapack_dir = spec['lapack'].prefix
            lapack_lib = spec['lapack'].libs.ld_flags
            args.extend(["--with-lapack=%s" % lapack_lib])

        if 'metis' in spec:
            args.extend([
                '--with-metis=%s' % spec['metis'].libs.ld_flags,
                '--with-metis-inc-dir=%s' % spec['metis'].prefix.include])

        if '+debug' in spec:
            args.append('--enable-gpudbg')
            args.append('--enable-analdbg')

        return args
