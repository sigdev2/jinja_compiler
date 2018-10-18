#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Copyright 2018, SigDev

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License. '''

from setuptools import setup, find_packages
from os.path import join, dirname, realpath
import jinja_compiler

setup(name=jinja_compiler.__name__,
      version=jinja_compiler.__version__,
      packages=find_packages(exclude=['example']),
      description='Compile Jinja2 templates to Python byte code',
      long_description=open(join(dirname(__file__), 'README.rst')).read(),
      author=jinja_compiler.__author__,
      license=jinja_compiler.__license__,
      url="http://github.com/sigdev2/jinja_compiler",
      keywords=' '.join([
        'jinja2', 'python', 'templates', 'compile'
        ]
      ),
      classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "Intended Audience :: System Administrators",
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        "Topic :: Software Development",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        ],
      install_requires=['jinja2>=2.8'],
      entry_points={
        'console_scripts': [
          'jinja_compiler = jinja_compiler.__main__:main',
          ]
      },
      zip_safe=False
)
