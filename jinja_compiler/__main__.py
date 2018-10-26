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

import argparse
import re
import json
import os.path
import sys
import glob
import codecs

from .jjcompiler import compile_jinja
from . import __version__, __copyright__

class ArgumentParser(argparse.ArgumentParser):    
    def _get_action_from_name(self, name):
        r'''Given a name, get the Action instance registered with this parser.
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

def is_define(string, encoding=r'utf-8', from_file = False):
        names = glob.glob(string)
        if len(names) > 0:
            ret = []
            for name in names:
                with codecs.open(name, encoding=encoding) as f:
                    try:
                        json_object = json.loads(f.read(), encoding=encoding)
                        ret.append(json_object)
                    except ValueError as e:
                        try:
                            ret.append(is_define(f.read(), encoding, True))
                        except argparse.ArgumentTypeError as e:
                            raise argparse.ArgumentTypeError('\'%r\' incorect vars file: \'%r\'' % string, str(e))
            return ret

        if string.startsWith(r'{') and string.endsWith(r'}'):
            try:
                if from_file:
                    json_object = json.loads(string, encoding=encoding)
                else:
                    json_object = json.loads(string)
                return json_object
            except ValueError as e:
                argparse.ArgumentTypeError('\'%r\' incorect json: \'%r\'' % string, str(e))

        out = {}
        for m in re.finditer(r'([A-z][A-z0-9]*)\=(([A-z_0-9]+)|\'([^\']*)\'|\"([^\"]*)\")', string, re.MULTILINE):
            if m == None:
                raise argparse.ArgumentTypeError('\'%r\' is not a var define' % m.string)
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

def check_encoding(enc):
    try:
        codecs.lookup(enc)
    except LookupError as e:
        raise argparse.ArgumentTypeError('\'%r\' incorect encoding: \'%r\'' % enc, str(e))

def get_from_args(args, key):
    if key in args:
        i = args.index(key)
        if i + 1 >= len(args):
            raise argparse.ArgumentTypeError('No value for argument \'%r\'' % key)
        val = args[i + 1]
        check_encoding(val)
        return (key, val)

    return (None, None)

def main(args):
    encoding = r'utf-8'
    arg = get_from_args(args, r'-c')
    if arg != (None, None):
        encoding = arg[1]
    else:
        arg = get_from_args(args, r'--encoding')
        if arg != (None, None):
            encoding = arg[1]

    parser = ArgumentParser(prog=r'python -m %r' % __loader__.fullname,
                            description=r'Jinja2 templates compiler to Python byte code',
                            epilog= __copyright__)

    parser.add_argument(r'template', nargs=1, type=file_or_template, help='Main Jinja2 template text or file, or files mask, where get fisrt match with mask, with Jinja2 template, enter point. If is inline template, then his id will be set as \'__main__\'')
    parser.add_argument(r'--include', r'-i', nargs=1, action=r'append', type=file_or_template, help=r'Add Jinja2 template text or file|files mask with Jinja2 template '\
                                                                           r'for search templates from loader. Inline templates wil be set id as $$N.jinja2, where N - number of template starts with zero')
    parser.add_argument(r'--out', r'-o', nargs=1, type=str, metavar=r'NAME', help=r'Name of zipfile (if --zip seted), file (if is CLI mode) or directory to save output. If out not cpecifed, then create random name and echo his, or in CLI mode out to colnsol')
    parser.add_argument(r'--var', r'-D', nargs=1, action=r'append', type=lambda x : is_define(x, encoding), metavar=r'VARS', help='Run as CLI mode. Use VARS as list of NAME=(VAL|\'VAL\'|"VAL"),'\
                                                                                 r' or single definition, or json format text, or as'\
                                                                                 r' file|files mask with json or definition formats declarations. Declare VARS'\
                                                                                 r' in global space for template')
    parser.add_argument(r'--ext', r'-e', nargs=1, action=r'append', type=str, metavar=r'EXTENSION', help=r'Add Jinja2 EXTENSION to templates environment')
    parser.add_argument(r'--zip', r'-z', nargs=r'?', choices=[r'deflated', r'stored'], help=r'If this flag exist, then all files store to zip archive. Ignore in CLI mode')
    parser.add_argument(r'--no-pyc', r'-C', nargs=r'?', type=bool, defaul=False, help=r'Disable save to py-compiled format, save as py-script. Ignore in CLI mode')
    parser.add_argument(r'--force', r'-f', nargs=r'?', type=bool, defaul=False, help=r'Overwrite not changed files. Ignore in CLI mode')
    parser.add_argument(r'--file-extension', r'-E', nargs=1, action=r'append', type=bool, defaul=False, help=r'Strict extensions to copile files. Ignore in CLI mode')
    parser.add_argument(r'--encoding', r'-c', nargs=1, type=check_encoding, defaul=r'utf-8', help=r'Work files encoding')

    r''' Jinja2 env args '''
    parser.add_argument(r'--block-start', r'-bs', nargs=1, type=str, defaul=r'{%', help=r'The string marking the beginning of a block')
    parser.add_argument(r'--block-end', r'-be', nargs=1, type=str, defaul=r'%}', help=r'The string marking the end of a block')
    parser.add_argument(r'--variable-start', r'-vs', nargs=1, type=str, defaul=r'{{', help=r'The string marking the beginning of a print statement')
    parser.add_argument(r'--variable-end', r'-ve', nargs=1, type=str, defaul=r'}}', help=r'The string marking the end of a print statement')
    parser.add_argument(r'--comment-start', r'-cs', nargs=1, type=str, defaul=r'{#', help=r'The string marking the beginning of a comment')
    parser.add_argument(r'--comment-end', r'-ce', nargs=1, type=str, defaul=r'#}', help=r'The string marking the end of a comment')
    
    parser.add_argument(r'--line-statement-prefix', r'-ls', nargs=1, type=str, help=r'If given and a string, this will be used as prefix for line based statements')
    parser.add_argument(r'--line-comment-prefix', r'-lc', nargs=1, type=str, help=r'If given and a string, this will be used as prefix for line based comments')
    
    parser.add_argument(r'--trim', r'-tm', nargs=r'?', type=bool, defaul=False, help=r'If this is set to True the first newline after a block is removed (block, not variable tag!)')
    parser.add_argument(r'--strp', r'-sp', nargs=r'?', type=bool, defaul=False, help=r'If this is set to True leading spaces and tabs are stripped from the start of a line to a block')
    parser.add_argument(r'--newline-sequence', r'-ns', nargs=1, type=str, defaul='\n', help='The sequence that starts a newline. Must be one of \'\r\', \'\n\' or \'\r\n\'')
    parser.add_argument(r'--keep-trailing-newline', r'-kn', nargs=r'?', type=bool, defaul=False, help=r'Preserve the trailing newline when rendering templates')
    
    parser.add_argument(r'--no-optimized', r'-no', nargs=r'?', type=bool, defaul=False, help=r'Disable Jinja2 optimizer')
    parser.add_argument(r'--no-autoescape', r'-na', nargs=r'?', type=bool, defaul=False, help=r'Disable Jinja2 autoescape')
    parser.add_argument(r'--cache', r'-ch', nargs=1, type=int, defaul=400, help=r'The size of the cache. If the cache size is set to 0 templates are recompiled all the time, if the cache size is -1 the cache will not be cleaned')
    parser.add_argument(r'--no-auto-reload', r'-nr', nargs=r'?', type=bool, defaul=False, help=r'Disable Jinja2 auto reload template. Some loaders load templates from locations where the template sources may change (ie: file system or database)')
    parser.add_argument(r'--async', r'-as', nargs=r'?', type=bool, defaul=False, help=r'If set to true this enables async template execution which allows you to take advantage of newer Python features. This requires Python 3.6 or later')
    
    parser.add_argument(r'--version', r'-v', action=r'version', version=(r'%r %s' % __loader__.fullname, __version__))

    options = parser.parse_args(args)
    
    ret = compile_jinja(options)
    if ret != None:
        print(ret)

    return 0

if __name__ == r'__main__':
    sys.exit(main(sys.argv[1:]))
