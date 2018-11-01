#!/usr/bin/env python
# -*- coding: utf-8 -*-

r''' Copyright 2018, SigDev

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License. '''

import os
import sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), r'..')))
import jinja_compiler
from jinja_compiler.__main__ import main

if __name__ == r'__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    main([r'class_cpp.jinja2', 
          r'-i', r'{%', r'if', r'property', r'%}{{property}};{%', r'endif', r'%}',
          r'-E', r'jinja2',
          r'-D', r'template_args="typename T"',
          r'-D', r'ns=ParentParentNS::ParentNS',
          r'-D', r'name=MyClass',
          r'-D', r'parent=ParentClass<T>',
          r'-D', r'args="int arg"',
          r'-D', r'parent_args=arg',
          r'-D', r'property="int prop"'])