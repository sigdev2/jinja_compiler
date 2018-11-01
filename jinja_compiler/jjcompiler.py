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
import re
import sys
import tempfile
import shutil
import codecs

import jinja2
from jinja2 import ChoiceLoader
from jinja2 import DictLoader
from jinja2 import FileSystemLoader
from jinja2 import ModuleLoader

class JJCoplilerOptions:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return None
    def get(self, key, d):
        if key in self.__dict__ and self.__dict__[key] != None:
            return self.__dict__[key]
        return d

def convertPath(path):
    sep = os.path.sep
    if sep != r'/':
        path = path.replace(sep, r'/')
    return path

def get_module_filename(filename, py_compile=False):
    module_filename = jinja2.ModuleLoader.get_module_filename(filename)
    if py_compile:
        module_filename += r'c'
    return module_filename

def make_filter(target, env, temp_folder, extensions=None, all_files=False, py_compile=False):
    def filter_func(tpl):
        if extensions is not None:
            ext = os.path.splitext(tpl)[1][1:]
            if ext not in extensions:
                return False
        if tpl.startswith(temp_folder + r'/'):
            return False
        if all_files:
            return True
      
        _content, filename, _update = env.loader.get_source(env, tpl)
        module_filename = os.path.join(target, get_module_filename(tpl, py_compile))
        if not os.path.exists(module_filename):
            return True
        return os.path.getmtime(filename) > os.path.getmtime(module_filename)

    return filter_func

r''' exports '''

def load_precompiled(options, tpl, folder):
    if not isinstance(options, JJCoplilerOptions):
        options = JJCoplilerOptions(**options)
    env = create_env(options, ModuleLoader(folder))
    return env.get_template(tpl)

def create_env(options, loaders):
    if not isinstance(options, JJCoplilerOptions):
        options = JJCoplilerOptions(**options)
    env_options = dict(
		block_start_string = options.get(r'block-start', r'{%'),
		block_end_string = options.get(r'block-end', r'%}'),
		variable_start_string = options.get(r'variable-start', r'{{'),
		variable_end_string = options.get(r'variable-end', r'}}'),
		comment_start_string = options.get(r'comment-start', r'{#'),
		comment_end_string = options.get(r'comment-end', r'#}'),
        line_statement_prefix = options.get(r'line-statement-prefix', None),
        line_comment_prefix = options.get(r'line-comment-prefix', None),
        trim_blocks = options.get(r'trim', False),
        lstrip_blocks = options.get(r'strp', False),
        newline_sequence = options.get(r'newline-sequence', '\n'),
        keep_trailing_newline = options.get(r'keep-trailing-newline', False),
        optimized = not options.get(r'no-optimized', False),
		autoescape = not options.get(r'no-autoescape', False),
        cache_size = options.get(r'cache', 400),
		auto_reload = not options.get(r'no-auto-reload', False),
        enable_async = options.get(r'async', False)
	)

    return jinja2.Environment(loader=loaders, extensions=options.get(r'ext', []), **env_options)

def compile_jinja(options):
    if not isinstance(options, JJCoplilerOptions):
        options = JJCoplilerOptions(**options)
    
    encoding = options.get(r'encoding', r'utf-8')

    r''' check input '''
    if options.template == None or len(options.template) < 1:
        return
    
    r''' input data '''
    temp_files = next(tempfile._get_candidate_names())
    dirs = [convertPath(os.getcwd()), temp_files]
    all_files = []
    dict_tpls = {}
    last_data = 0
    
    r''' template entry point '''
    template_id = r'__main__'
    if isinstance(options.template, list):
        tpl_path = convertPath(os.path.abspath(options.template[0]))
        dir_name = os.path.dirname(tpl_path)
        if dir_name not in dirs:
            dirs.append(dir_name)
        all_files.append(tpl_path)
        mtime = os.path.getmtime(tpl_path)
        if last_data < mtime:
            last_data = mtime
        template_id = os.path.basename(tpl_path)
    else:
        dict_tpls[template_id] = options.template
    
    r''' consulidate template includes'''
    n = 0
    for t in options.get(r'include', []):
        if isinstance(t, list):
            for tpl_file in t:
                tpl_file = convertPath(os.path.abspath(tpl_file))
                dir_name = os.path.dirname(tpl_file)
                if dir_name not in dirs:
                    dirs.append(dir_name)
                all_files.append(tpl_file)
                mtime = os.path.getmtime(tpl_file)
                if last_data < mtime:
                    last_data = mtime
        else:
            dict_tpls[r'$$' + str(n) + r'.jinja2'] = t
            n += 1


    r''' create loaders '''
    if len(dirs) == 1:
        dirs = dirs[0]
    templateLoader = ChoiceLoader([
        DictLoader(dict_tpls),
        FileSystemLoader(searchpath=dirs, followlinks=True, encoding=r'utf-8')
    ])

    r''' fill environment '''
    templateEnv = create_env(options, templateLoader)

    r''' force rewrite '''
    is_zip = options.zip and options.var == None
    is_single = is_zip or options.var != None
    is_rewrite = options.get(r'force', False)
    out_file = options.out
    if out_file == None:
        is_rewrite = True
    else:
        if is_single:
            if is_zip:
                out_file += r'.zip'
            if os.path.exists(out_file):
                is_rewrite = is_rewrite or len(dict_tpls) > 0 or last_data > os.path.getmtime(out_file)
                if not is_rewrite:
                    print(r'The output file is newer')
                    return
            else:
                is_rewrite = True
        elif not os.path.exists(out_file):
            is_rewrite = True
    
    r''' temp file '''
    temp_file = options.out
    if is_single:
        temp_file = next(tempfile._get_candidate_names())

    r''' compile '''
    try:
        if options.var == None:
            if options.out != None:
                os.makedirs(temp_files)
                for tpl in dict_tpls.keys():
                    with codecs.open(os.path.join(temp_files, tpl), r'w', encoding=encoding) as f:
                        f.write(dict_tpls[tpl])
                exts = options.get(r'file-extension', [])
                if not isinstance(exts, list):
                    exts = [exts]
                filter_func = make_filter(temp_file, templateEnv, temp_files, exts, is_rewrite, not options[r'no-pyc'])
                templateEnv.compile_templates(temp_file, extensions=None,
                    filter_func=filter_func, zip=(options.zip if options.zip else None), ignore_errors=False, py_compile=not options[r'no-pyc'])
                shutil.rmtree(temp_files)
            else:
                print(r'No input file')
        else:
            props = {}
            for var_set in options.var:
                if isinstance(var_set, list):
                    for json in var_set:
                        for key in json.keys():
                            props[key] = json[key]
                else:
                    for key in var_set.keys():
                        props[key] = var_set[key]

            template = templateEnv.get_template(template_id)
            if out_file == None:
                return template.render(props)
            else:
                with codecs.open(temp_file, r'w', encoding=encoding) as f:
                    f.write(template.render(props))
    except Exception as e:
        print(str(e))
        if temp_file != None and os.path.exists(temp_file):
            if is_single:
                os.remove(temp_file)
            else:
                shutil.rmtree(temp_file)
        if os.path.exists(temp_files):
            shutil.rmtree(temp_files)
        return
    
    r''' replace result files '''
    if out_file != None and is_single and is_rewrite and os.path.exists(temp_file):
        if os.path.exists(out_file):
            os.remove(out_file)
        os.rename(temp_file, out_file)
    
if __name__ == r'__main__':  
    pass