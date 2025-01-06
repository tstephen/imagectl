###############################################################################
# Copyright 2024 Tim Stephenson and contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License.  You may obtain a copy
#  of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under
#  the License.
#
# Command line client for managing an image library.
#
###############################################################################
import argparse
import hashlib
import importlib
import inspect
import logging
import sys

import imagectl.cmds
from imagectl.api import ImageCommand, ImageCommandOptions
from imagectl.constants import TOOL

logger = logging.getLogger(__name__)
commands: dict

def get_hash(in_file: str) -> str:
    """returns the hash of the specified file"""
    with open(in_file, 'rb') as f:
        hasher = hashlib.md5()
        hasher.update(f.read())
        in_hash=hasher.hexdigest()
        logger.debug('hash of %s is %s', in_file, in_hash)
    return in_hash

def init_logging(args): 
    """initialise logging system"""
    if args.verbose is None:
        args.verbose = 'WARNING'
    logging.basicConfig() #NOSONAR
    logger.setLevel(args.verbose)
    logger.info("log verbosity set to %s", args.verbose)

def register_commands(parser):
    """locate and instantiate all the commands available"""
    logger.info('registering commands')

    cmd_parsers = parser.add_subparsers(dest='command')
    commands = {}
    for mod_name in imagectl.cmds.__all__:
        logger.info('importing commands from %s', mod_name)
        module = importlib.import_module('imagectl.cmds.'+mod_name)
        for _, clazz in inspect.getmembers(module, inspect.isclass):
            if issubclass(clazz, ImageCommand) and not inspect.isabstract(clazz):
                logger.info('  registering %s', clazz)
                cmd = clazz(cmd_parsers)
                commands[cmd.NAME] = cmd
    return commands

def exec_cmd(cmd: str, options: ImageCommandOptions):
    try:
        commands[cmd].execute(options)
    except ValueError as err:
        logger.error(err)
        commands[cmd].cmd.print_help(sys.stderr)
        sys.exit(1)

def main():
    '''Main entry point'''

    parser = argparse.ArgumentParser(prog=TOOL.get("name"))
    parser.add_argument("-v", "--verbose", help="increase output verbosity")
    parser._positionals.title = "commands"

    global commands
    commands = register_commands(parser)
    args = parser.parse_args()
    init_logging(args)

    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        exec_cmd(args.command, args)

if __name__ == "main":
    main()