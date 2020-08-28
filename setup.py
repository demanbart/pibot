from distutils.core import setup

setup(name='pibot',
      version='0.1',
      description='Python robot development tools',
      author='Bart Deman',
      author_email='b.deman@dbcon.be',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['pibot', 'pibot.communicate', 'pibot.control', 'pibot.motor'],
	  requires=['pygame','sys','time'],
     )