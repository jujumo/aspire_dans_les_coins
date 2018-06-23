# import ads.parsing.ParserCollection
# import ads.parsing.ParsingLeboncoin

from importlib import import_module
from os.path import realpath, dirname, join, basename, splitext
from glob import glob

INIT_NAME = realpath(__file__)
MODULE_PATH = dirname(realpath(__file__))

parser_list = [f for f in glob(join(MODULE_PATH, '*.py')) if not f == INIT_NAME]
for modulename in parser_list:
    modulename = 'ads.parsing.' + splitext(basename(modulename))[0]
    # print(f'auto import {modulename}')
    new_module = import_module(modulename)
