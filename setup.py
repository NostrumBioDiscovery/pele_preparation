#!/usr/bin/env python

from distutils.core import setup

setup(name='pele_preparation',
      version='1.0',
      description='Python scripts to prepare PELE input',
      packages=['PPP', 'Helpers'],
      install_requires=[ 'prody==1.8.2', 'pandas', 'scipy'],
      include_package_data=True,
      author='Daniel Soler',
      author_email='daniel.soler@nostrumbiodiscovery.com',
      url='https://github.com/NostrumBioDiscovery/pele_preparation',
     )
