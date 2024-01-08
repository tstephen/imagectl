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
import hashlib
import logging
import os
from os.path import join, getctime, getmtime, getsize
from time import ctime, strftime

from imagectl.api import ImageCommand, ImageCommandOptions
from imagectl.constants import TOOL
from imagectl.models import IndexEntry

logger = logging.getLogger(__name__)

class IndexCommand(ImageCommand):
    """Command to index an image library"""
    NAME = 'index'
    valid_extensions = [".jpg", ".jpeg", ".png"]

    def __init__(self, subparsers):
        super().__init__(self)
        self.cmd = subparsers.add_parser(self.NAME,
                   help='index an image library')
        self.cmd.add_argument("-i", "--input", help="base image directory")

    def execute(self, options: ImageCommandOptions):
        logger.setLevel(options.verbose)
        if options.input[-1:] == '/':
            options.input = options.input[:-1]
        logger.info("indexing %s", options.input)

        index = []
        for root, dirs, files in os.walk(options.input):
            dir = root[len(options.input)+1:] if root.index(options.input) > -1 else ''
            logger.info("...%s", dir)
            for name in files:
                if name[0] == '.':
                    continue # ignore hidden files
                qual_name = join(root, name)
                rel_name = join(dir, name)
                logger.debug("...%s", rel_name)
                entry = IndexEntry(name=rel_name,
                                    created=datetime.fromtimestamp(getctime(qual_name)).isoformat(),
                                    modified=datetime.fromtimestamp(getmtime(qual_name)).isoformat(),
                                    size=getsize(qual_name))
                entry.calc_hash(qual_name)
                index.append(entry)
        with open(join(options.input, f'.{TOOL.get("name")}'), 'w') as out:
            for entry in index:
                out.write(entry.model_dump())
