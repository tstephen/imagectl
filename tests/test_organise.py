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


def test_get_new_file_name_no_optimisations():
    assert OrganiserCommand.get_new_file_name("foo.png", "2025", "01", "03") == "2025-01-03-foo.png"

def test_get_new_file_name_avoid_dupe_date():
    assert OrganiserCommand.get_new_file_name("2025-01-03-foo.png", "2025", "01", "03") == "2025-01-03-foo.png"
