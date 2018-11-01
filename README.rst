Jinja2 compiler
===================================

Jinja2 templates compiler to Python byte code.

Console usage:

    usage: jinja_compiler [-h] [--include INCLUDE [INCLUDE ...]]
                          [--out NAME [NAME ...]] [--var VARS [VARS ...]]
                          [--ext EXTENSION] [--zip [{deflated,stored}]]
                          [--no-pyc [NO_PYC]] [--force [FORCE]]
                          [--file-extension FILE_EXTENSION] [--encoding ENCODING]
                          [--block-start BLOCK_START [BLOCK_START ...]]
                          [--block-end BLOCK_END [BLOCK_END ...]]
                          [--variable-start VARIABLE_START [VARIABLE_START ...]]
                          [--variable-end VARIABLE_END [VARIABLE_END ...]]
                          [--comment-start COMMENT_START [COMMENT_START ...]]
                          [--comment-end COMMENT_END [COMMENT_END ...]]
                          [--line-statement-prefix LINE_STATEMENT_PREFIX [LINE_STATEMENT_PREFIX ...]]
                          [--line-comment-prefix LINE_COMMENT_PREFIX [LINE_COMMENT_PREFIX ...]]
                          [--trim [TRIM]] [--strp [STRP]]
                          [--newline-sequence NEWLINE_SEQUENCE [NEWLINE_SEQUENCE ...]]
                          [--keep-trailing-newline [KEEP_TRAILING_NEWLINE]]
                          [--no-optimized [NO_OPTIMIZED]]
                          [--no-autoescape [NO_AUTOESCAPE]] [--cache CACHE]
                          [--no-auto-reload [NO_AUTO_RELOAD]] [--async [ASYNC]]
                          [--version]
                          template [template ...]

    Jinja2 templates compiler to Python byte code

    positional arguments:
      template              Main Jinja2 template text or file, or files mask,
                            where get fisrt match with mask, with Jinja2 template,
                            enter point. If is inline template, then his id will
                            be set as '__main__'

    optional arguments:
      -h, --help            show this help message and exit
      --include INCLUDE [INCLUDE ...], -i INCLUDE [INCLUDE ...]
                            Add Jinja2 template text or file|files mask with
                            Jinja2 template for search templates from loader.
                            Inline templates wil be set id as $$N.jinja2, where N
                            - number of template starts with zero
      --out NAME [NAME ...], -o NAME [NAME ...]
                            Name of zipfile (if --zip seted), file (if is CLI
                            mode) or directory to save output. If out not
                            cpecifed, then create random name and echo his, or in
                            CLI mode out to colnsol
      --var VARS [VARS ...], -D VARS [VARS ...]
                            Run as CLI mode. Use VARS as list of
                            NAME=(VAL|'VAL'|"VAL"), or single definition, or json
                            format text, or as file|files mask with json or
                            definition formats declarations. Declare VARS in
                            global space for template
      --ext EXTENSION, -e EXTENSION
                            Add Jinja2 EXTENSION to templates environment
      --zip [{deflated,stored}], -z [{deflated,stored}]
                            If this flag exist, then all files store to zip
                            archive. Ignore in CLI mode
      --no-pyc [NO_PYC], -C [NO_PYC]
                            Disable save to py-compiled format, save as py-script.
                            Ignore in CLI mode
      --force [FORCE], -f [FORCE]
                            Overwrite not changed files. Ignore in CLI mode
      --file-extension FILE_EXTENSION, -E FILE_EXTENSION
                            Strict extensions to copile files. Ignore in CLI mode
      --encoding ENCODING, -c ENCODING
                            Work files encoding
      --block-start BLOCK_START [BLOCK_START ...], -bs BLOCK_START [BLOCK_START ...]
                            The string marking the beginning of a block
      --block-end BLOCK_END [BLOCK_END ...], -be BLOCK_END [BLOCK_END ...]
                            The string marking the end of a block
      --variable-start VARIABLE_START [VARIABLE_START ...], -vs VARIABLE_START [VARIABLE_START ...]
                            The string marking the beginning of a print statement
      --variable-end VARIABLE_END [VARIABLE_END ...], -ve VARIABLE_END [VARIABLE_END ...]
                            The string marking the end of a print statement
      --comment-start COMMENT_START [COMMENT_START ...], -cs COMMENT_START [COMMENT_START ...]
                            The string marking the beginning of a comment
      --comment-end COMMENT_END [COMMENT_END ...], -ce COMMENT_END [COMMENT_END ...]
                            The string marking the end of a comment
      --line-statement-prefix LINE_STATEMENT_PREFIX [LINE_STATEMENT_PREFIX ...], -ls LINE_STATEMENT_PREFIX [LINE_STATEMENT_PREFIX ...]
                            If given and a string, this will be used as prefix for
                            line based statements
      --line-comment-prefix LINE_COMMENT_PREFIX [LINE_COMMENT_PREFIX ...], -lc LINE_COMMENT_PREFIX [LINE_COMMENT_PREFIX ...]
                            If given and a string, this will be used as prefix for
                            line based comments
      --trim [TRIM], -tm [TRIM]
                            If this is set to True the first newline after a block
                            is removed (block, not variable tag!)
      --strp [STRP], -sp [STRP]
                            If this is set to True leading spaces and tabs are
                            stripped from the start of a line to a block
      --newline-sequence NEWLINE_SEQUENCE [NEWLINE_SEQUENCE ...], -ns NEWLINE_SEQUENCE [NEWLINE_SEQUENCE ...]
                            The sequence that starts a newline. Must be one of '
                            ', ' ' or ' '
      --keep-trailing-newline [KEEP_TRAILING_NEWLINE], -kn [KEEP_TRAILING_NEWLINE]
                            Preserve the trailing newline when rendering templates
      --no-optimized [NO_OPTIMIZED], -no [NO_OPTIMIZED]
                            Disable Jinja2 optimizer
      --no-autoescape [NO_AUTOESCAPE], -na [NO_AUTOESCAPE]
                            Disable Jinja2 autoescape
      --cache CACHE, -ch CACHE
                            The size of the cache. If the cache size is set to 0
                            templates are recompiled all the time, if the cache
                            size is -1 the cache will not be cleaned
      --no-auto-reload [NO_AUTO_RELOAD], -nr [NO_AUTO_RELOAD]
                            Disable Jinja2 auto reload template. Some loaders load
                            templates from locations where the template sources
                            may change (ie: file system or database)
      --async [ASYNC], -as [ASYNC]
                            If set to true this enables async template execution
                            which allows you to take advantage of newer Python
                            features. This requires Python 3.6 or later
      --version, -v         show program's version number and exit

    Copyright 2018, SigDev
