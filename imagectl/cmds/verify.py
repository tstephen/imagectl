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
import logging
from os.path import join

from pydantic_core import ValidationError

from imagectl.api import ImageCommand, ImageCommandOptions
from imagectl.constants import TOOL
from imagectl.models import IndexEntry

logger = logging.getLogger(__name__)

class VerifyCommand(ImageCommand):
    """Command to verify an image library"""
    NAME = 'verify'
    def __init__(self, subparsers):
        super().__init__(self)
        self.cmd = subparsers.add_parser(self.NAME,
                   help='verify images against index')
        self.cmd.add_argument("-i", "--input", help="base image directory")

    def execute(self, options: ImageCommandOptions):
        logger.setLevel(options.verbose)
        if options.input is None:
            raise ValueError("Input collection must be specified")
        logger.info("verifying %s", options.input)

        with open(join(options.input, f'.{TOOL.get("name")}'), 'r') as index:
            for line in index.readlines():
                try:
                    entry = IndexEntry.from_str(line)
                    qual_name = join(options.input, entry.name)
                    if entry.matches(qual_name):
                        logger.info('...%s is verified', entry.name)
                    elif entry.hash_matches(qual_name):
                        logger.info('...%s has the expected hash, update index', entry.name)
                    else:
                        logger.error("...%s has the wrong hash, investigate", entry.name)
                except ValidationError as ve:
                    logger.error('unable to parse %s', line)
                    continue
