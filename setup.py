from distutils.core import setup

setup(name='curbd',
      version='0.1',
      scripts=[
          'bin/curbd'
      ],
      url='https://github.com/ridecharge/curbd',
      packages=['curbd'],
      install_requires=['boto>=2.34.0', 'nose>=1.3.4', 'coverage>=3.7.1', 'python-consul>=0.3.3']
)
