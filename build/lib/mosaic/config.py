import os
import sys
import pathlib
import argparse
import configparser
import numpy as np
from collections import OrderedDict
from pathlib import Path

from mosaic import log
from mosaic import util

LOGS_HOME = Path.home()/'logs'
CONFIG_FILE_NAME = os.path.join(str(pathlib.Path.home()), 'mosaic.conf')

SHIFT_H_FILE_NAME = os.path.join(str(pathlib.Path.home()), 'shifts_h.txt')
SHIFT_V_FILE_NAME = os.path.join(str(pathlib.Path.home()), 'shifts_v.txt')

SECTIONS = OrderedDict()

SECTIONS['general'] = {
    'config': {
        'default': CONFIG_FILE_NAME,
        'type': str,
        'help': "File name of configuration",
        'metavar': 'FILE'},
    'logs-home': {
        'default': LOGS_HOME,
        'type': str,
        'help': "Log file directory",
        'metavar': 'FILE'},
    'verbose': {
        'default': True,
        'help': 'Verbose output',
        'action': 'store_true'},
        }

SECTIONS['file-io'] = {
    'folder-name': {
        'default': '.',
        'type': Path,
        'help': "Name of the last used directory containing multiple hdf files",
        'metavar': 'PATH'},
    'tmp-file-name': {
        'default': '/tile/tmp.h5',
        'type': str,
        'help': "Default output file name",
        'metavar': 'FILE'},
    'tile-file-name': {
        'default': 'tile.h5',
        'type': str,
        'help': "Default stitched file name",
        'metavar': 'FILE'},
    'file-format': {
        'default': 'dx',
        'type': str,
        'help': "see from https://dxchange.readthedocs.io/en/latest/source/demo.html",
        'choices': ['dx', 'aps2bm', 'aps7bm', 'aps32id']},
    'binning': {
        'type': util.positive_int,
        'default': 0,
        'help': "Reconstruction binning factor as power(2, choice)",
        'choices': [0, 1, 2, 3]},
    'sample-x': {     
        'type': str,
        'default': '/measurement/instrument/sample_motor_stack/setup/x',
        'help': "Location in the hdf tomography layout where to find the tile x position (mm)"},    
    'sample-y': {     
        'type': str,
        'default': '/measurement/instrument/sample_motor_stack/setup/y',
        'help': "Location in the hdf tomography layout where to find the tile y position (mm)"},    
    'resolution': {     
        'type': str,
        'default': '/measurement/instrument/detection_system/objective/resolution',
        'help': "Location in the hdf tomography layout where to find the image resolution (um)"},    
    'full_file_name': {     
        'type': str,
        'default': '/measurement/sample/file/full_name',
        'help': "Location in the hdf tomography layout where to find the full file name"},
    'step-x': {
        'default': 0,
        'type': float,
        'help': 'When greater than 0, it is used to manually overide the sample x step size stored in the hdf file'},  
    'chunk-size': {     
        'type': int,
        'default': 64,
        'help': "Number of of projections for simultaneous processing",},    
       }

SECTIONS['stitch'] = {
    'test': {
        'default': False,
        'help': 'if set one projection called mosaic_test will be stitched and placed in raw data folded',
        'action': 'store_true'},
    'nprojection': {     
        'type': float,
        'default': 0.5,
        'help': "Projection used for the stitching test",},
       }

SECTIONS['shift'] = {    
    'threshold': {
        'default': 0.5,
        'type': float,
        'help': 'Threshold for selecting matching features (0,1)'},
    'nprojection': {
        'type': float,
        'default': 0.5,
        'help': "Projection number (0,1)"},        
       }

SECTIONS['extract'] = {
    'nprojection': {
        'type': float,
        'default': 0.5,
        'help': "Projection number (0,1)"},        
    }

MOSAIC_PARAMS = ('file-io', )
STITCH_PARAMS = ('file-io', 'stitch')
SHIFT_PARAMS = ('file-io', 'shift')
EXTRACT_PARAMS = ('file-io', 'extract')

NICE_NAMES = ('General', 'File IO', 'Stitch')

def get_config_name():
    """Get the command line --config option."""
    name = CONFIG_FILE_NAME
    for i, arg in enumerate(sys.argv):
        if arg.startswith('--config'):
            if arg == '--config':
                return sys.argv[i + 1]
            else:
                name = sys.argv[i].split('--config')[1]
                if name[0] == '=':
                    name = name[1:]
                return name

    return name


def parse_known_args(parser, subparser=False):
    """
    Parse arguments from file and then override by the ones specified on the
    command line. Use *parser* for parsing and is *subparser* is True take into
    account that there is a value on the command line specifying the subparser.
    """
    if len(sys.argv) > 1:
        subparser_value = [sys.argv[1]] if subparser else []
        config_values = config_to_list(config_name=get_config_name())
        values = subparser_value + config_values + sys.argv[1:]
        #print(subparser_value, config_values, values)
    else:
        values = ""

    return parser.parse_known_args(values)[0]


def config_to_list(config_name=CONFIG_FILE_NAME):
    """
    Read arguments from config file and convert them to a list of keys and
    values as sys.argv does when they are specified on the command line.
    *config_name* is the file name of the config file.
    """
    result = []
    config = configparser.ConfigParser()

    if not config.read([config_name]):
        return []

    for section in SECTIONS:
        for name, opts in ((n, o) for n, o in SECTIONS[section].items() if config.has_option(section, n)):
            value = config.get(section, name)

            if value != '' and value != 'None':
                action = opts.get('action', None)

                if action == 'store_true' and value == 'True':
                    # Only the key is on the command line for this action
                    result.append('--{}'.format(name))

                if not action == 'store_true':
                    if opts.get('nargs', None) == '+':
                        result.append('--{}'.format(name))
                        result.extend((v.strip() for v in value.split(',')))
                    else:
                        result.append('--{}={}'.format(name, value))

    return result


class Params(object):
    def __init__(self, sections=()):
        self.sections = sections + ('general', )

    def add_parser_args(self, parser):
        for section in self.sections:
            for name in sorted(SECTIONS[section]):
                opts = SECTIONS[section][name]
                parser.add_argument('--{}'.format(name), **opts)

    def add_arguments(self, parser):
        self.add_parser_args(parser)
        return parser

    def get_defaults(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)

        return parser.parse_args('')


def write(config_file, args=None, sections=None):
    """
    Write *config_file* with values from *args* if they are specified,
    otherwise use the defaults. If *sections* are specified, write values from
    *args* only to those sections, use the defaults on the remaining ones.
    """
    config = configparser.ConfigParser()

    for section in SECTIONS:
        config.add_section(section)
        for name, opts in SECTIONS[section].items():
            if args and sections and section in sections and hasattr(args, name.replace('-', '_')):
                value = getattr(args, name.replace('-', '_'))
                if isinstance(value, list):
                    # print(type(value), value)
                    value = ', '.join(value)
            else:
                value = opts['default'] if opts['default'] is not None else ''

            prefix = '# ' if value == '' else ''

            if name != 'config':
                config.set(section, prefix + name, str(value))
    with open(config_file, 'w') as f:
        config.write(f)


def log_values(args):
    """Log all values set in the args namespace.

    Arguments are grouped according to their section and logged alphabetically
    using the DEBUG log level thus --verbose is required.
    """
    args = args.__dict__

    for section, name in zip(SECTIONS, NICE_NAMES):
        entries = sorted((k for k in args.keys() if k in SECTIONS[section]))
        if entries:
            log.info(name)
            for entry in entries:
                value = args[entry] if args[entry] is not None else "-"
                log.info("  {:<16} {}".format(entry, value))


def show_config(args):
    """Log all values set in the args namespace.

    Arguments are grouped according to their section and logged alphabetically
    using the DEBUG log level thus --verbose is required.
    """
    args = args.__dict__

    log.warning('mosaic status start')
    for section, name in zip(SECTIONS, NICE_NAMES):
        entries = sorted((k for k in args.keys() if k.replace('_', '-') in SECTIONS[section]))
        if entries:
            for entry in entries:
                value = args[entry] if args[entry] != None else "-"
                log.info("  {:<16} {}".format(entry, value))

    log.warning('mosaic status end')
 
