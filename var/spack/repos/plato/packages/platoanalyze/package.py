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


class Platoanalyze(CMakePackage):
    """Plato Analyze"""

    homepage = "https://github.com/platoengine/platoanalyze"
    url      = "https://github.com/platoengine/platoanalyze"
    git      = "https://github.com/platoengine/platoanalyze.git"

    maintainers = ['rviertel', 'jrobbin']

    version('release', branch='release', submodules=True)
    version('develop', branch='develop', submodules=True)
    version('tpl_update', branch='tpl_update', submodules=True) # remove before deployment

    variant( 'cuda',       default=True,     description='Compile with cuda'            )
    variant( 'mpmd',       default=True,     description='Compile with mpmd'            )
    variant( 'meshmap',    default=True,     description='Compile with MeshMap'         )
    variant( 'amgx',       default=True,     description='Compile with AMGX'            )
    variant( 'python',     default=True,     description='Compile with python'          )
    variant( 'esp',        default=True,     description='Compile with ESP'             )
    variant( 'geometry',   default=False,    description='Compile with MLS geometry'    )
    variant( 'openmp',     default=False,    description='Compile with openmp'          )
    variant( 'rocket',     default=False,    description='Builds ROCKET and ROCKET_MPMD')
    variant( 'tpetra',     default=False,    description='Compile with Tpetra'          )

# tpl_update
    variant('compute_capability', default='70', description="GPU compute capability",
        values=('30', '35', '37', '50', '52', '60', '61', '70', '75'))
#end

#    depends_on('trilinos+epetra')
#    depends_on('trilinos+cuda',                             when='+cuda')
#    depends_on('trilinos+openmp',                           when='+openmp')
#    depends_on('trilinos+tpetra+belos+ifpack2+amesos2+superlu+muelu',     when='+tpetra')
    depends_on('cmake@3.0.0:', type='build')

#    depends_on('platoengine~unit_testing+stk+iso',                       when='+mpmd'  )
#    depends_on('platoengine~unit_testing+stk+iso+geometry',              when='+geometry')
#    depends_on('platoengine~unit_testing+stk+iso~geometry',              when='~geometry')
#    depends_on('platoengine~unit_testing+stk+iso@develop',                when='@develop' )
    depends_on('python @2.6:2.999',                          when='+python')

# tpl_update
    depends_on('platoengine~unit_testing+stk+iso+expy+esp@tpl_update',            when='@tpl_update' )

#    depends_on('cuda @10.2.89', when='+cuda')
    depends_on('cuda @10.0.130', when='+cuda')

    # this pattern isn't elegant, but it works.  (Is there a better way to forward a variant value?)
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=75', when='@tpl_update compute_capability=75')
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=70', when='@tpl_update compute_capability=70')
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=61', when='@tpl_update compute_capability=61')
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=60', when='@tpl_update compute_capability=60')
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=52', when='@tpl_update compute_capability=52')
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=37', when='@tpl_update compute_capability=37')
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=35', when='@tpl_update compute_capability=35')
    depends_on('trilinos+cuda+wrapper+chaco~zoltan~zoltan2~tpetra+shards~muelu~ifpack~ifpack2~belos~amesos2~amesos~suite-sparse~hypre+intrepid@master cxxstd=14 cuda_arch=30', when='@tpl_update compute_capability=30')

    # this pattern isn't elegant, but it works.  (Is there a better way to forward a variant value?)
    depends_on('amgx cuda_arch=75', when='+amgx compute_capability=75')
    depends_on('amgx cuda_arch=70', when='+amgx compute_capability=70')
    depends_on('amgx cuda_arch=61', when='+amgx compute_capability=61')
    depends_on('amgx cuda_arch=60', when='+amgx compute_capability=60')
    depends_on('amgx cuda_arch=52', when='+amgx compute_capability=52')
    depends_on('amgx cuda_arch=37', when='+amgx compute_capability=37')
    depends_on('amgx cuda_arch=35', when='+amgx compute_capability=35')
    depends_on('amgx cuda_arch=30', when='+amgx compute_capability=30')
#end


#    depends_on('platoengine~unit_testing+stk+iso@release',               when='@release' )
#    depends_on('platoengine~unit_testing+stk+iso+esp',                   when='+mpmd+esp')

    depends_on('arborx~mpi~cuda~serial @header_only',       when='+meshmap')
    depends_on('amgx',                                      when='+amgx')
    depends_on('omega-h @develop',                           type=('build', 'link', 'run'))
    depends_on('esp',                                       when='+esp')

    conflicts('+geometry', when='~mpmd')
    conflicts('+meshmap',  when='~mpmd')
    conflicts('+amgx',     when='~cuda')

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

          omega_h_dir = spec['omega-h'].prefix
          options.extend([ '-DOMEGA_H_PREFIX:PATH={0}'.format(omega_h_dir) ])

        if '~mpmd' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_MPMD=OFF' ])

        if '+python' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_PYTHON=ON' ])

        if '+geometry' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_GEOMETRY=ON' ])

        if '+meshmap' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_MESHMAP=ON' ])

        if '+tpetra' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_TPETRA=ON' ])
          superlu_dir = spec['superlu'].prefix
          options.extend([ '-DSuperLU_PREFIX:PATH={0}'.format(superlu_dir) ])

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


        return options

    def setup_environment(self, spack_env, run_env):

        if '+python' in self.spec:
          run_env.prepend_path('PYTHONPATH', self.prefix.lib)
