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
import abc

from pydantic import BaseModel

class ImageCommandOptions(BaseModel):
    """A model object containing options that target Command understoods"""

class ImageCommand(abc.ABC):
    """A command encapsulates one piece of functionality"""
    @abc.abstractmethod
    def __init__(self, subparsers):
        """initialise any classes and data required to execute this command"""

    @abc.abstractmethod
    def execute(self, options: ImageCommandOptions):
        """run the command"""
