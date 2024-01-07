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
import os
from os.path import join, getctime, getmtime, getsize

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
        logger.info("indexing %s", options.input)

        index = []
        for root, dirs, files in os.walk(options.input):
            for name in files:
                qualified_name = join(root, name)
                index.append(IndexEntry(name=qualified_name[len(options.input)+1:],
                                        created=getctime(qualified_name),
                                        modified=getmtime(qualified_name),
                                        size=getsize(qualified_name)))
        with open(join(options.input, f'.{TOOL.get("name")}'), 'w') as out:
            for entry in index:
                out.write(entry.model_dump())
