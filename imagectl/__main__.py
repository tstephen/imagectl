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
import importlib
import inspect
import logging
import sys

import imagectl.cmds
from imagectl.api import ImageCommand
from imagectl.constants import TOOL

logger = logging.getLogger(__name__)

def init_logging(args): 
    """initialise logging system"""
    if args.verbose is None:
        args.verbose = 'INFO'
    logging.basicConfig() #NOSONAR
    logger.setLevel(args.verbose)
    logger.warning("log verbosity set to %s", args.verbose)

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

def main():
    '''Main entry point'''

    parser = argparse.ArgumentParser(prog=TOOL.get("name"))
    parser.add_argument("-v", "--verbose", help="increase output verbosity")
    parser._positionals.title = "commands"

    commands = register_commands(parser)
    args = parser.parse_args()
    init_logging(args)

    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        commands[args.command].execute(args)

if __name__ == "main":
    main()