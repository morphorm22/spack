# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install moris
#
# You can edit this file again by typing:
#
#     spack edit moris
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Moris(CMakePackage):

    homepage = "https://www.example.com"
    git      = "ssh://titan/home/git/codes/moris"

    version('plato', branch='plato')

    depends_on('mpi', type=('build','link','run'))
    depends_on('arpack-ng')
    depends_on('superlu')
    depends_on('superlu-dist')
    depends_on('hdf5+cxx~debug+fortran+hl+mpi+pic+shared~szip~threadsafe')
    depends_on('trilinos~adios2~alloptpkgs+amesos~amesos2+anasazi+aztec+belos+boost~cgns+chaco~complex~cuda~cuda_rdc~debug~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran+glm~gtest+hdf5~hwloc+hypre+ifpack+ifpack2+intrepid~intrepid2~ipo~isorropia+kokkos+kokkoskernels+matio~mesquite+metis~minitensor+ml+mpi+muelu~mumps+netcdf~nox~openmp~pamgen~percept~phalanx~piro+pnetcdf~python~rol~rythmos+sacado+shards+shared~shylu+stk~stratimikos~strumpack+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~wrapper~x11~xsdkflags+zlib+zoltan+zoltan2 build_type=RelWithDebInfo cuda_arch=none cxxstd=14 gotype=int')
    depends_on('boost')
    depends_on('petsc')
    depends_on('armadillo')
    #depends_on('intel-mkl')


    def cmake_args(self):
        options = []
        options.extend(['-DBUILD_ALL=OFF'])
        options.extend(['-DBUILD_ALG=ON'])
        options.extend(['-DBUILD_ASR=ON'])
        options.extend(['-DBUILD_CHR=ON'])
        options.extend(['-DBUILD_COM=ON'])
        options.extend(['-DBUILD_CON=ON'])
        options.extend(['-DBUILD_DLA=ON'])
        options.extend(['-DBUILD_EXA=ON'])
        options.extend(['-DBUILD_EXC=ON'])
        options.extend(['-DBUILD_FEM=OFF'])
        options.extend(['-DBUILD_GEN=ON'])
        options.extend(['-DBUILD_HMR=ON'])
        options.extend(['-DBUILD_INT=OFF'])
        options.extend(['-DBUILD_IOS=ON'])
        options.extend(['-DBUILD_LINALG=ON'])
        options.extend(['-DBUILD_MDL=OFF'])
        options.extend(['-DBUILD_MSI=OFF'])
        options.extend(['-DBUILD_MTK=ON'])
        options.extend(['-DBUILD_MAP=ON'])
        options.extend(['-DBUILD_NLA=ON'])
        options.extend(['-DBUILD_OPT=OFF'])
        options.extend(['-DBUILD_SDF=OFF'])
        options.extend(['-DBUILD_STK=OFF'])
        options.extend(['-DBUILD_TSA=OFF'])
        options.extend(['-DBUILD_TOL=ON'])
        options.extend(['-DBUILD_VIS=ON'])
        options.extend(['-DBUILD_XTK=ON'])
        options.extend(['-DBUILD_WRK=OFF'])
        options.extend(['-DBUILD_MAI=ON'])
        options.extend(['-DMORIS_USE_OPENBLAS=ON'])
        options.extend(['-DMORIS_USE_TESTS=OFF'])
        return options
