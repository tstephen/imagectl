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
from imagectl.api import ImageCommand, ImageCommandOptions

class IndexCommand(ImageCommand):
    """Command to organise an image library"""
    NAME = 'organise'
    def __init__(self, subparsers):
        super().__init__(self)
        self.cmd = subparsers.add_parser(self.NAME,
                   help='organise images in a standard structure')

    def execute(self, options: ImageCommandOptions):
        print(f'command {self.NAME} not yet implemented')
