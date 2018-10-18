#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')))
import jinja_compiler


vars_list = {
        'templat_args': 'typename T',
        'ns' : 'ParentParentNS::ParentNS',
        'name' : 'MyClass',
        'parent' : 'ParentClass<T>',
        'args' : 'int arg',
        'parent_args' : 'arg',
        'property': 'int prop'
    }
options = {
    'template' : ['class_cpp.jinja2'],
    'include' : ['{% if property %}{{property}};{% endif %}'],
    'out' : None,
    'var' : [vars_list],
    'ext' : [],
    'zip' : False,
    'no-pyc' : False,
    'force' : False,
    'file-extension' : ['jinja2'],
    'no-autoescape' : True
}

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    print('CLI mode example:\n')
    out1 = jinja_compiler.compile_jinja(options)
    print(out1)
    print('\n========\n')

    print('Compile templates:\n')
    options['out'] = 'test_binarys'
    options['var'] = None
    jinja_compiler.compile_jinja(options)

    tpl = jinja_compiler.load_precompiled(options, 'class_cpp.jinja2', 'test_binarys')
    out2 = tpl.render(vars_list)
    print(out2)
    print('\n========\n')

    print('\nOuts is equal: ' + ('True' if out1 == out2 else 'Flase'))