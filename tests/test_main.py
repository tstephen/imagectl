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
###############################################################################
from imagectl.cmds.organise import OrganiserCommand
import os


def test_is_writable_file_does_not_exist():
    assert OrganiserCommand.is_writable(f"tests{os.sep}resources{os.sep}in{os.sep}Bird.jpg",
                                        f"tests{os.sep}resources{os.sep}out{os.sep}NotExistant.jpg") == True

def test_is_writable_file_exists_and_same_hash():
    assert OrganiserCommand.is_writable(f"tests{os.sep}resources{os.sep}in{os.sep}Frog.jpg",
                                        f"tests{os.sep}resources{os.sep}out{os.sep}Frog.jpg") == True

def test_is_writable_file_exists_and_different_hash():
    assert OrganiserCommand.is_writable(f"tests{os.sep}resources{os.sep}in{os.sep}Bird.jpg",
                                        f"tests{os.sep}resources{os.sep}out{os.sep}Frog.jpg") == False

def test_is_writable_file_exists_and_same_name_diff_hash():
    assert OrganiserCommand.is_writable(f"tests{os.sep}resources{os.sep}in{os.sep}Bird.jpg",
                                        f"tests{os.sep}resources{os.sep}out{os.sep}Bird.jpg") == False
