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
from datetime import datetime
import logging
import os
from os.path import exists, join, splitext
from shutil import move

from pydantic_core import ValidationError
from imagectl.__main__ import exec_cmd

from imagectl.api import ImageCommand, ImageCommandOptions
from imagectl.cmds.index import IndexCommandOptions
from imagectl.constants import TOOL
from imagectl.models import IndexEntry

logger = logging.getLogger(__name__)

class DedupeCommand(ImageCommand):
    """Command to deduplicate an image library"""
    NAME = 'dedupe'
    def __init__(self, subparsers):
        super().__init__(self)
        self.cmd = subparsers.add_parser(self.NAME,
                   help='identify duplicates between 2 image libraries')
        self.cmd.add_argument("-e", "--exec", action="store_true",
                               help="perform the recommended actions")
        self.cmd.add_argument("-r", "--reference", help="reference image directory")
        self.cmd.add_argument("-t", "--target", help="directory to search for duplicates")

    def execute(self, options: ImageCommandOptions):
        logger.setLevel(options.verbose)
        if options.reference is None or options.target is None:
            raise ValueError("Both reference and target collections must be specified")

        logger.info("searching %s\nfor files already in %s",
                    options.target, options.reference)

        ref_idx = join(options.reference, f'.{TOOL.get("name")}')
        if not exists(ref_idx):
            exec_cmd('index', IndexCommandOptions(
                input=options.reference, verbose=options.verbose))
        with open(ref_idx, 'r') as index:
            self.ref_entries = [IndexEntry.from_str(line)
                                for line in index.readlines()]
            self.ref_by_name = {entry.name: entry for entry in self.ref_entries}

        trgt_idx = join(options.target, f'.{TOOL.get("name")}')
        if not exists(trgt_idx):
            exec_cmd('index', IndexCommandOptions(
                input=options.target, verbose=options.verbose))
        with open(trgt_idx, 'r') as index:
            for line in index.readlines():
                try:
                    entry = IndexEntry.from_str(line)
                    if entry.name in self.ref_by_name:
                        ref = self.ref_by_name.get(entry.name)
                        if entry.hash == ref.hash:
                            logger.warning('...%s is matched, delete from target', entry.name)
                            if options.exec is True:
                                os.remove(join(options.target, entry.name))
                        else:
                            logger.warning('...%s is different in reference, target file must be renamed', entry.name)
                            if options.exec is True:
                                parts = splitext(entry.name)
                                now = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                                move(join(options.target, entry.name),
                                    join(options.reference, f'{parts[0]}.{now}{parts[1]}'))
                    else:
                        logger.warning(f'...%s to be added to reference', entry.name)
                        if options.exec is True:
                            move(join(options.target, entry.name),
                                 join(options.reference, entry.name))
                except ValidationError as ve:
                    logger.error('unable to parse %s', line)
                    continue
