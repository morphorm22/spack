# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ipopt(AutotoolsPackage):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
       software package for large-scale nonlinear optimization."""
    homepage = "https://projects.coin-or.org/Ipopt"
    url      = "https://github.com/lanl-ansi/Ipopt/archive/refs/tags/releases/3.13.3.tar.gz"

    version('3.13.3', sha256='86354b36c691e6cd6b8049218519923ab0ce8a6f0a432c2c0de605191f2d4a1c')

    variant('coinhsl', default=False,
            description="Build with Coin Harwell Subroutine Libraries")
    variant('metis',   default=False,
            description="Build with METIS partitioning support")
    variant('mumps',   default=False,
            description="Build with MUMPS solver")
    variant('spral',   default=True,
            description="Build with SPRAL solver")
    variant('debug',   default=False,
            description="Build debug instead of optimized version")

    depends_on("blas")
    depends_on("netlib-lapack")
    depends_on("mpi",              when='~mumps')
    depends_on("pkgconfig",        type='build')
    depends_on("mumps+double~mpi", when='+mumps')
    depends_on("spral",            when='+spral')
    depends_on('coinhsl',          when='+coinhsl')
    depends_on('metis@4.0:',       when='+metis')

    patch('ipopt_ppc_build.patch', when='arch=ppc64le')

    # IPOPT does not build correctly in parallel on OS X
    parallel = False

    def configure_args(self):
        spec = self.spec
        # Dependency directories
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix

        blas_lib = spec['blas'].libs.ld_flags
        lapack_lib = spec['lapack'].libs.ld_flags

        args = [
            "--prefix=%s" % self.prefix,
            "--enable-shared",
            "coin_skip_warn_cxxflags=yes",
            "--with-blas-incdir=%s" % blas_dir.include,
            "--with-blas-lib=%s" % blas_lib,
            "--with-lapack-incdir=%s" % lapack_dir.include,
            "--with-lapack-lib=%s" % lapack_lib
        ]

        if 'mumps' in spec:
            mumps_dir = spec['mumps'].prefix

            # Add directory with fake MPI headers in sequential MUMPS
            # install to header search path
            mumps_flags = "-ldmumps -lmumps_common -lpord -lmpiseq"
            mumps_libcmd = "-L%s " % mumps_dir.lib + mumps_flags

            args.extend([
                "--with-mumps-incdir=%s" % mumps_dir.include,
                "--with-mumps-lib=%s" % mumps_libcmd])

        if 'spral' in spec:
            spral_dir = spec['spral'].prefix
            spral_ld_flags = spec['spral'].libs.ld_flags
            args.extend([
                "--with-spral-lflags=-L%s %s" % (spral_dir.lib, spral_ld_flags),
                "--with-mumps-lib=-I%s" % spral_dir.include])

        if 'coinhsl' in spec:
            args.extend([
                '--with-hsl-lib=%s' % spec['coinhsl'].libs.ld_flags,
                '--with-hsl-incdir=%s' % spec['coinhsl'].prefix.include])

        if 'metis' in spec:
            args.extend([
                '--with-metis-lib=%s' % spec['metis'].libs.ld_flags,
                '--with-metis-incdir=%s' % spec['metis'].prefix.include])

        # The IPOPT configure file states that '--enable-debug' implies
        # '--disable-shared', but adding '--enable-shared' overrides
        # '--disable-shared' and builds a shared library with debug symbols
        if '+debug' in spec:
            args.append('--enable-debug')
        else:
            args.append('--disable-debug')

        return args
