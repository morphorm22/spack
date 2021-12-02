# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Platoengine(CMakePackage):
    """Plato Engine - Platform for Topology Optimization"""
    
    homepage = "https://www.sandia.gov/plato3d/"
    url      = "https://github.com/platoengine/platoengine/archive/v0.6.0.tar.gz"
    git      = "https://github.com/platoengine/platoengine.git"

    maintainers = ['rviertel', 'jrobbin']

    version('develop', branch='develop', preferred=True)

    variant( 'platomain',      default=True,    description='Compile PlatoMain'               )
    variant( 'platostatics',   default=True,    description='Compile PlatoStatics'            )
    variant( 'regression',     default=True,    description='Add regression tests'            )
    variant( 'ipopt',          default=False,   description='Compile with IPOPT for MMA'      )
    variant( 'unit_testing',   default=True,    description='Add unit testing'                )
    variant( 'albany_tests',   default=False,   description='Configure Albany tests'          )
    variant( 'analyze_tests',  default=False,   description='Configure Analyze tests'         )
    variant( 'cuda',           default=False,   description='Compile with cuda'               )
    variant( 'esp',            default=False,    description='Turn on esp'                    )
    variant( 'expy',           default=False,   description='Compile exodus/python API'       )
    variant( 'geometry',       default=False,   description='Turn on Plato Geometry'          )
    variant( 'iso',            default=False,   description='Turn on iso extraction'          )
    variant( 'platoproxy',     default=False,   description='Compile PlatoProxy'              )
    variant( 'prune',          default=False,   description='Turn on use of prune and refine' )
    variant( 'rol',            default=False,   description='Turn on use of rol'              )
    variant( 'stk',            default=False,   description='Turn on use of stk'              )
    variant( 'xtk',            default=False,   description='Turn on use of xtk'              )
    variant( 'tpetra_tests',   default=False,   description='Configure Tpetra tests'          )
    variant( 'dakota',         default=False,   description='Compile with Dakota'             )
    variant( 'services',       default=False,   description='Compile with services'           )

    conflicts( '+expy', when='-platomain')
    conflicts( '+iso',  when='-stk')
    conflicts( '+prune',  when='-stk')
    conflicts( '@0.1.0', when='+prune')
    conflicts( '@0.2.0', when='+prune')
    conflicts( '@0.3.0', when='+prune')
    conflicts( '@0.4.0', when='+prune')
    conflicts( '@0.5.0', when='+prune')
    conflicts( '@0.6.0', when='+prune')
    conflicts( '+prune', when='+dakota')
    conflicts( '+rol',   when='+dakota')
    conflicts( '+expy', when='+dakota')

    depends_on( 'ipopt@3.12.8', when='+ipopt')
    depends_on( 'trilinos+exodus+chaco+intrepid+shards gotype=int')
    depends_on( 'trilinos@13.0.1 cxxstd=11',                                         when='+dakota')
    depends_on( 'mpi',            type=('build','link','run'))
    depends_on( 'cmake@3.19.5:',   type='build')
    depends_on( 'trilinos@rol_update+rol cxxstd=14',                           when='+rol')
    depends_on( 'trilinos+zlib+pnetcdf+boost \
                                       +stk',           when='+stk')
    depends_on( 'trilinos@rol_update+percept+zoltan+zlib+pnetcdf+boost \
                                       +stk cxxstd=14',           when='+prune')
    depends_on( 'trilinos+zlib+pnetcdf+boost+intrepid2 \
                             +minitensor+pamgen',             when='+geometry')
    depends_on( 'trilinos+zlib+pnetcdf+boost \
                                       +stk~gtest+hdf5+ifpack+amesos+belos+muelu+tpetra~mumps+zoltan2+zoltan',           when='+stk')

    depends_on( 'googletest',                                 when='+unit_testing' )
    depends_on( 'python@2.6:2.999', type=('build', 'link', 'run'), when='+expy'    )
    depends_on( 'nlopt',                                      when='+expy'         )
    # py-setuptools later than v44.1.0 require python 3.x
    depends_on( 'py-numpy@1.16.5 ^py-setuptools@44.1.0',      when='+expy'         )
    depends_on( 'trilinos+cuda+wrapper',                              when='+cuda')

    depends_on( 'esp', when='+esp')
    depends_on( 'moris@plato', when='+xtk')
    depends_on( 'hdf5+cxx~debug+fortran+hl+mpi+pic+shared~szip~threadsafe',when='+stk')
    depends_on( 'arpack-ng',when='+xtk')
    depends_on( 'superlu',when='+xtk')
    depends_on( 'superlu-dist',when='+xtk')
    
    depends_on( 'dakota', when='+dakota')
    depends_on( 'numdiff', when='+analyze_tests+esp+dakota')

    def cmake_args(self):
        spec = self.spec

        options = []

        trilinos_dir = spec['trilinos'].prefix
        options.extend([ '-DSEACAS_PATH:FILEPATH={0}'.format(trilinos_dir) ])
        options.extend([ '-DTRILINOS_INSTALL_DIR:FILEPATH={0}'.format(trilinos_dir) ])

        if '+platomain' in spec:
          options.extend([ '-DPLATOMAIN=ON' ])

        if '+ipopt' in spec:
          options.extend([ '-DIPOPT_ENABLED=ON' ])
          ipopt_dir = spec['ipopt'].prefix
          options.extend([ '-DIPOPT_INSTALL_DIR:FILEPATH={0}'.format(ipopt_dir) ])
        
        if '+platoproxy' in spec:
          options.extend([ '-DPLATOPROXY=ON' ])

        if '+platostatics' in spec:
          options.extend([ '-DPLATOSTATICS=ON' ])

        if '+expy' in spec:
          options.extend([ '-DEXPY=ON' ])
          options.extend([ '-DPLATO_ENABLE_SERVICES_PYTHON=ON' ])

        if '+regression' in spec:
          options.extend([ '-DREGRESSION=ON' ])
          options.extend([ '-DSEACAS=ON' ])

        if '+unit_testing' in spec:
          options.extend([ '-DUNIT_TESTING=ON' ])
          gtest_dir = spec['googletest'].prefix
        else:
          options.extend([ '-DUNIT_TESTING=OFF' ])

          options.extend([ '-DGTEST_HOME:FILEPATH={0}'.format(gtest_dir) ])

        if '+iso' in spec:
          options.extend([ '-DENABLE_ISO=ON' ])

        if '+prune' in spec:
          options.extend([ '-DENABLE_PRUNE=ON' ])

        if '+geometry' in spec:
          options.extend([ '-DGEOMETRY=ON' ])

        if '+stk' in spec:
          options.extend([ '-DSTK_ENABLED=ON' ])

        if '+xtk' in spec:
          options.extend([ '-DXTK_ENABLED=ON' ])
        if '~xtk' in spec:
          options.extend([ '-DXTK_ENABLED=OFF' ])

        if '+esp' in spec:
          options.extend([ '-DESP_ENABLED=ON' ])
          esp_lib_dir = spec['esp'].prefix+'/lib'
          esp_inc_dir = spec['esp'].prefix+'/include'
          options.extend([ '-DESP_LIB_DIR:PATH={0}'.format(esp_lib_dir) ])
          options.extend([ '-DESP_INC_DIR:PATH={0}'.format(esp_inc_dir) ])

        if '+rol' in spec:
          options.extend([ '-DENABLE_ROL=ON' ])

        if '-stk' in spec:
          options.extend([ '-DSTK_ENABLED=OFF' ])

        if '+albany_tests' in spec:
          options.extend([ '-DALBANY=ON' ])
          options.extend([ '-DALBANY_BINARY=AlbanyMPMD' ])

        if '+analyze_tests' in spec:
          options.extend([ '-DANALYZE=ON' ])
          options.extend([ '-DANALYZE_BINARY=analyze_MPMD' ])

        if '+tpetra_tests' in spec:
          options.extend([ '-DPLATO_TPETRA=ON' ])

        if '+dakota' in spec:
          options.extend([ '-DDAKOTADRIVER=ON' ])
          boost_dir = spec['boost'].prefix
          options.extend([ '-DBOOST_ROOT:FILEPATH={0}'.format(boost_dir) ])
          options.extend([ '-DCMAKE_CXX_COMPILER_VERSION={0}'.format(spec.compiler.version)])

        if '+services' in spec:
          options.extend([ '-DENABLE_PLATO_SERVICES=ON' ])
        if '+analyze_tests+esp+dakota' in spec:
          numdiff_dir = spec['numdiff'].prefix
          options.extend([ '-DNUMDIFF_PATH:FILEPATH={0}'.format(numdiff_dir) ])

        return options


    def setup_environment(self, spack_env, run_env):

        if '+expy' in self.spec:
          run_env.prepend_path('PYTHONPATH', self.prefix.lib)
          run_env.prepend_path('PYTHONPATH', self.prefix.etc)
          

        run_env.prepend_path('PATH', self.prefix.etc)
