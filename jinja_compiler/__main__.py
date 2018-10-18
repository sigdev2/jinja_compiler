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

import argparse
import re
import json
import os.path
import sys
import glob

from .jjcompiler import compile_jinja
from . import __version__, __copyright__

class ArgumentParser(argparse.ArgumentParser):    
    def _get_action_from_name(self, name):
        '''Given a name, get the Action instance registered with this parser.
        If only it were made available in the ArgumentError object. It is 
        passed as it's first arg...'''
        container = self._actions
        if name is None:
            return None
        for action in container:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action

    def error(self, message):
        exc = sys.exc_info()[1]
        if exc:
            exc.argument = self._get_action_from_name(exc.argument_name)
            raise exc
        super(ArgumentParser, self).error(message)

def is_define(string):
        names = glob.glob(string)
        if len(names) > 0:
            ret = []
            for name in names:
                with open(name) as f:
                    try:
                        json_object = json.loads(name)
                        ret.append(json_object)
                    except ValueError as e:
                        try:
                            ret.append(is_define(f.read()))
                        except argparse.ArgumentTypeError as e:
                            raise argparse.ArgumentTypeError("\'%r\' incorect vars file: \'%r\'" % string, str(e))
            return ret

        if string.startsWith('{') and string.endsWith('}'):
            try:
                json_object = json.loads(string)
                return json_object
            except ValueError as e:
                argparse.ArgumentTypeError("\'%r\' incorect json: \'%r\'" % string, str(e))

        out = {}
        for m in re.finditer(r"([A-z][A-z0-9]*)\=(([A-z_0-9]+)|\'([^\']*)\'|\"([^\"]*)\")", string, re.MULTILINE):
            if m == None:
                raise argparse.ArgumentTypeError("\'%r\' is not a var define" % m.string)
            name, val, text, quoted, dquoted = m.groups()
            if val == None:
                val = text
            if val == None:
                val = quoted
            if val == None:
                val = dquoted
            out[name] = val

        return out

def file_or_template(string):
    names = glob.glob(string)
    if len(names) > 0:
        return names
    return string

def main(args):
    parser = ArgumentParser(prog='python -m %r' % __loader__.fullname,
                            description='Jinja2 templates compiler to Python byte code',
                            epilog= __copyright__)

    parser.add_argument('template', nargs=1, type=file_or_template, help='Main Jinja2 template text or file, or files mask, where get fisrt match with mask, with Jinja2 template, enter point. If is inline template, then his id will be set as \'__main__\'')
    parser.add_argument('--include', '-i', nargs=1, action='append', type=file_or_template, help='Add Jinja2 template text or file|files mask with Jinja2 template '\
                                                                           'for search templates from loader. Inline templates wil be set id as $$N.jinja2, where N - number of template starts with zero')
    parser.add_argument('--out', '-o', nargs=1, type=str, metavar='NAME', help='Name of zipfile (if --zip seted), file (if is CLI mode) or directory to save output. If out not cpecifed, then create random name and echo his, or in CLI mode out to colnsol')
    parser.add_argument('--var', '-D', nargs=1, action='append', type=is_define, metavar='VARS', help='Run as CLI mode. Use VARS as list of NAME=(VAL|\'VAL\'|"VAL"),'\
                                                                                 ' or single definition, or json format text, or as'\
                                                                                 ' file|files mask with json or definition formats declarations. Declare VARS'\
                                                                                 ' in global space for template')
    parser.add_argument('--ext', '-e', nargs=1, action='append', type=str, metavar='EXTENSION', help='Add Jinja2 EXTENSION to templates environment')
    parser.add_argument('--zip', '-z', nargs='?', choices=['deflated', 'stored'], help='If this flag exist, then all files store to zip archive. Ignore in CLI mode')
    parser.add_argument('--no-pyc', '-C', nargs='?', type=bool, defaul=False, help='Disable save to py-compiled format, save as py-script. Ignore in CLI mode')
    parser.add_argument('--force', '-f', nargs='?', type=bool, defaul=False, help='Overwrite not changed files. Ignore in CLI mode')
    parser.add_argument('--file-extension', '-E', nargs='1', action='append', type=bool, defaul=False, help='Strict extensions to copile files. Ignore in CLI mode')

    ''' Jinja2 env args '''
    parser.add_argument('--block-start', '-bs', nargs=1, type=str, defaul='{%', help='The string marking the beginning of a block')
    parser.add_argument('--block-end', '-be', nargs=1, type=str, defaul='%}', help='The string marking the end of a block')
    parser.add_argument('--variable-start', '-vs', nargs=1, type=str, defaul='{{', help='The string marking the beginning of a print statement')
    parser.add_argument('--variable-end', '-ve', nargs=1, type=str, defaul='}}', help='The string marking the end of a print statement')
    parser.add_argument('--comment-start', '-cs', nargs=1, type=str, defaul='{#', help='The string marking the beginning of a comment')
    parser.add_argument('--comment-end', '-ce', nargs=1, type=str, defaul='#}', help='The string marking the end of a comment')
    
    parser.add_argument('--line-statement-prefix', '-ls', nargs=1, type=str, help='If given and a string, this will be used as prefix for line based statements')
    parser.add_argument('--line-comment-prefix', '-lc', nargs=1, type=str, help='If given and a string, this will be used as prefix for line based comments')
    
    parser.add_argument('--trim', '-tm', nargs='?', type=bool, defaul=False, help='If this is set to True the first newline after a block is removed (block, not variable tag!)')
    parser.add_argument('--strp', '-sp', nargs='?', type=bool, defaul=False, help='If this is set to True leading spaces and tabs are stripped from the start of a line to a block')
    parser.add_argument('--newline-sequence', '-ns', nargs=1, type=str, defaul='\n', help='The sequence that starts a newline. Must be one of \'\r\', \'\n\' or \'\r\n\'')
    parser.add_argument('--keep-trailing-newline', '-kn', nargs='?', type=bool, defaul=False, help='Preserve the trailing newline when rendering templates')
    
    parser.add_argument('--no-optimized', '-no', nargs='?', type=bool, defaul=False, help='Disable Jinja2 optimizer')
    parser.add_argument('--no-autoescape', '-na', nargs='?', type=bool, defaul=False, help='Disable Jinja2 autoescape')
    parser.add_argument('--cache', '-ch', nargs=1, type=int, defaul=400, help='The size of the cache. If the cache size is set to 0 templates are recompiled all the time, if the cache size is -1 the cache will not be cleaned')
    parser.add_argument('--no-auto-reload', '-nr', nargs='?', type=bool, defaul=False, help='Disable Jinja2 auto reload template. Some loaders load templates from locations where the template sources may change (ie: file system or database)')
    parser.add_argument('--async', '-as', nargs='?', type=bool, defaul=False, help='If set to true this enables async template execution which allows you to take advantage of newer Python features. This requires Python 3.6 or later')
    
    parser.add_argument('--version', '-v', action='version', version=('%r %s' % __loader__.fullname, __version__))

    options = parser.parse_args(args)
    
    ret = compile_jinja(options)
    if ret != None:
        print(ret)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
