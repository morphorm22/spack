##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Platoanalyze(CMakePackage, CudaPackage):
    """Plato Analyze"""

    homepage = "https://github.com/platoengine/platoanalyze"
    url      = "https://github.com/platoengine/platoanalyze"
    git      = "https://github.com/platoengine/platoanalyze.git"

    maintainers = ['rviertel', 'jrobbin']

    version('develop', branch='develop', submodules=True, preferred=True)
    version('release-v0.1.0', branch='release-v0.1.0', submodules=True)

    variant( 'cuda',       default=True,     description='Compile with Nvidia CUDA'     )
    variant( 'amgx',       default=True,     description='Compile with AMGX'            )
    variant( 'meshmap',    default=True,     description='Compile with MeshMap'         )
    variant( 'mpmd',       default=True,     description='Compile with mpmd'            )
    variant( 'physics',    default=True,     description='Compile with all Physics'      )
    variant( 'helmholtz',  default=True,     description='Compile with Helmholtz filter' )
    variant( 'unittests',  default=True,     description='Compile with unit tests' )
    variant( 'enginemesh', default=True,     description='Compile with enginemesh as default' )
    variant( 'omega-h',    default=False,    description='Compile with enginemesh as default' )
    variant( 'esp',        default=False,    description='Compile with ESP'             )
    variant( 'geometry',   default=False,    description='Compile with MLS geometry'    )
    variant( 'openmp',     default=False,    description='Compile with openmp'          )
    variant( 'python',     default=False,    description='Compile with python'          )
    variant( 'rocket',     default=False,    description='Builds ROCKET and ROCKET_MPMD')
    variant( 'tpetra',     default=False,    description='Compile with Tpetra'          )
    variant( 'epetra',     default=True,     description='Compile with Epetra'          )
    variant( 'verificationtests', default=False, description='Compile with verification tests' )

    depends_on('platoengine+analyze_tests',                                       when='+mpmd')
    depends_on('trilinos@13.4+kokkos+kokkoskernels+exodus gotype=int cxxstd=14')
    depends_on('trilinos+cuda+wrapper', when='+cuda')
    depends_on('trilinos+openmp', when='+openmp')
    depends_on('trilinos+tpetra+belos+ifpack2+amesos2+muelu+zoltan2',             when='+tpetra')
    depends_on('trilinos~tpetra~amesos2~ifpack2~belos~muelu~zoltan2',             when='~tpetra')
    depends_on('trilinos~epetra',                                                 when='~epetra')
    depends_on('trilinos+pamgen',                                                 when='+geometry')
    depends_on('platoengine+geometry',                                            when='+geometry')
    depends_on('platoengine~dakota',                                              when='+cuda+mpmd')
    depends_on('cmake@3.0.0:', type='build')
    depends_on('python @3.8:',                               when='+python')
    depends_on('platoengine+expy',                           when='+python')
    depends_on('netlib-lapack')

    depends_on('arborx~mpi~cuda~serial @v1.1',              when='+meshmap')
    depends_on('amgx',                                      when='+amgx')
    depends_on('esp',                                       when='+esp')
    depends_on('python @3.8:',                              when='+esp@121Lin')
    depends_on('python @3.8:',                              when='+esp@120Lin')
    depends_on('platoengine+esp',                           when='+esp')

    depends_on('paraview+python3 build_edition=canonical',  when='+verificationtests')
    depends_on('gnuplot',  when='+verificationtests')

    conflicts('+enginemesh', when='~mpmd')
    conflicts('+geometry', when='~mpmd')
    conflicts('+meshmap',  when='~mpmd')
    conflicts('+amgx',     when='~cuda')
    conflicts('+openmp',   when='+cuda')
    depends_on('omega-h@develop_bb6b', type=('build', 'link', 'run'), when='+omega-h')
    depends_on('omega-h+cuda',                              when='+cuda+omega-h')

    conflicts('~epetra',    when='~tpetra')
    conflicts('~omega-h',   when='~enginemesh')
    conflicts('+unittests', when='~physics')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([ '-DBUILD_SHARED_LIBS:BOOL=ON' ])

        trilinos_dir = spec['trilinos'].prefix
        options.extend([ '-DTrilinos_PREFIX:PATH={0}'.format(trilinos_dir) ])

        if '+mpmd' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_MPMD=ON' ])

          platoengine_dir = spec['platoengine'].prefix
          options.extend([ '-DPLATOENGINE_PREFIX:PATH={0}'.format(platoengine_dir) ])

        else:
          options.extend([ '-DPLATOANALYZE_ENABLE_MPMD=OFF' ])

        if '+omega-h' in spec:
          omega_h_dir = spec['omega-h'].prefix
          options.extend([ '-DOMEGA_H_PREFIX:PATH={0}'.format(omega_h_dir) ])

        if '+python' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_PYTHON=ON' ])

        if '+enginemesh' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_ENGINEMESH=ON' ])

        if '+geometry' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_GEOMETRY=ON' ])

        if '+cuda' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_CUDA=ON' ])

        if '+meshmap' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_MESHMAP=ON' ])

        if '+tpetra' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_TPETRA=ON' ])

        if '+epetra' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_EPETRA=ON' ])

        if '+esp' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_ESP=ON' ])
          esp_lib_dir = spec['esp'].prefix+'/lib'
          esp_inc_dir = spec['esp'].prefix+'/include'
          options.extend([ '-DESP_LIB_DIR:PATH={0}'.format(esp_lib_dir) ])
          options.extend([ '-DESP_INC_DIR:PATH={0}'.format(esp_inc_dir) ])

        if '+amgx' in spec:
          amgx_dir = spec['amgx'].prefix
          options.extend([ '-DAMGX_PREFIX:PATH={0}'.format(amgx_dir) ])

        if '+rocket' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_ROCKET=ON' ])
          
        if '~physics' in spec:
          options.extend([ '-DELLIPTIC=OFF' ])
          options.extend([ '-DPARABOLIC=OFF' ])
          options.extend([ '-DHYPERBOLIC=OFF' ])
          options.extend([ '-DSTABILIZED=OFF' ])
          options.extend([ '-DPLASTICITY=OFF' ])

        if '+helmholtz' in spec:
          options.extend([ '-DHELMHOLTZ=ON' ])

        if '~helmholtz' in spec:
          options.extend([ '-DHELMHOLTZ=OFF' ])

        if '~unittests' in spec:
          options.extend([ '-DPLATOANALYZE_UNIT_TEST=OFF' ])

        if '+verificationtests' in spec:
          options.extend(['-DPLATOANALYZE_SMOKE_TESTS=ON'])
        elif '~verificationtests' in spec:
          options.extend(['-DPLATOANALYZE_SMOKE_TESTS=OFF'])

        return options

    def setup_environment(self, spack_env, run_env):

        if '+python' in self.spec:
          run_env.prepend_path('PYTHONPATH', self.prefix.lib)
