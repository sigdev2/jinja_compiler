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

import sys
import os

import sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), r'..')))
import jinja_compiler


vars_list = {
        r'template_args': r'typename T',
        r'ns' : r'ParentParentNS::ParentNS',
        r'name' : r'MyClass',
        r'parent' : r'ParentClass<T>',
        r'args' : r'int arg',
        r'parent_args' : r'arg',
        r'property': r'int prop'
    }
options = {
    r'template' : [r'class_cpp.jinja2'],
    r'include' : [r'{% if property %}{{property}};{% endif %}'],
    r'out' : None,
    r'var' : [vars_list],
    r'ext' : [],
    r'zip' : False,
    r'no-pyc' : False,
    r'force' : False,
    r'file-extension' : [r'jinja2'],
    r'no-autoescape' : True
}

if __name__ == r'__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    print('CLI mode example:\n')
    out1 = jinja_compiler.compile_jinja(options)
    print(out1)
    print('\n========\n')

    print('Compile templates:\n')
    options[r'out'] = r'test_binarys'
    options[r'var'] = None
    jinja_compiler.compile_jinja(options)

    tpl = jinja_compiler.load_precompiled(options, r'class_cpp.jinja2', r'test_binarys')
    out2 = tpl.render(vars_list)
    print(out2)
    print('\n========\n')

    print('\nOuts is equal: ' + (r'True' if out1 == out2 else r'Flase'))