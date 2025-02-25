from distutils.dir_util import copy_tree
from spack import *

class Esp(Package):
    """Engineering SketchPad by Bob Haimes at MIT"""

    homepage = "https://acdl.mit.edu/ESP/"

    version('121Lin', sha256='c9ed01f6acf2cc1b0d2a035a563efa8e0ab5b857269fdd6776596abffc98dc89', url='https://acdl.mit.edu/ESP/archive/ESP121Lin.tgz',preferred=True)
    version('120Lin', sha256='d16c7d90d4e1b46973113e47f474b59057df35f9bd55680c3430aface1571ba9', url='https://acdl.mit.edu/ESP/archive/ESP120Lin.tgz')
    version('117Lin', sha256='bd6418ee9dafabdc17c58449c379535f4f148f1f67730074297c605b5e10e1a0', url='https://acdl.mit.edu/ESP/archive/ESP117Lin.tgz')

    depends_on( 'python@2.6:', type=('run'), when='@117Lin' )
    depends_on( 'python@3.8:', type=('run'), when='@120Lin' )
    depends_on( 'python@3.8:', type=('run'), when='@121Lin' )

    phases = ['install']


    def install(self, spec, prefix):

      copy_tree('EngSketchPad/lib', prefix.lib)

      if (spec.satisfies('@121Lin')):
        copy_tree('OpenCASCADE-7.6.0/lib', prefix.lib)
        copy_tree('EngSketchPad/pyESP', prefix.pyESP)
      elif (spec.satisfies('@120Lin')):
        copy_tree('OpenCASCADE-7.4.1/lib', prefix.lib)
        copy_tree('EngSketchPad/pyESP', prefix.pyESP)
      elif (spec.satisfies('@117Lin')):
        copy_tree('OpenCASCADE-7.3.1/lib', prefix.lib)

      copy_tree('EngSketchPad/include', prefix.include)

      copy_tree('EngSketchPad/bin', prefix.bin)

      copy_tree('EngSketchPad/src', prefix.src)

      copy_tree('EngSketchPad/ESP', prefix.ESP)

    def setup_run_environment(self, run_env):

      if (self.spec.satisfies('@117Lin')):
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
      else:
        run_env.prepend_path('PYTHONPATH', self.prefix.pyESP)

      run_env.set('ESP_START', 'google-chrome '+self.prefix.ESP+'/ESP-localhost7681.html')
      run_env.set('UDUNITS2_XML_PATH', self.prefix+'/src/CAPS/udunits/udunits2.xml')
      run_env.set('ESP_ROOT', self.prefix)
      run_env.set('ESP_ARCH', 'LINUX64')
      if (self.spec.satisfies('@117Lin')):
        run_env.set('CASREV', '7.3')
      if (self.spec.satisfies('@120Lin')):
        run_env.set('CASREV', '7.4')
      if (self.spec.satisfies('@121Lin')):
        run_env.set('CASREV', '7.6')

