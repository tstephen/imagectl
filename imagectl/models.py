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
from hmac import compare_digest
import logging
from os.path import join, getctime, getmtime, getsize
from urllib.parse import quote

from pydantic import BaseModel, model_serializer

logger = logging.getLogger(__name__)

class IndexEntry(BaseModel):
    """An index entry"""
    name: str
    created: str
    modified: str
    size: int
    hash: str = None

    def calc_hash(self, qual_name: str):
        with open(qual_name, 'rb') as afile:
            hasher = hashlib.md5()
            hasher.update(afile.read())
            self.hash=hasher.hexdigest()

    def matches(self, qual_name: str) -> bool:
        return (self.size == getsize(qual_name) \
                and self.created == datetime.fromtimestamp(getctime(qual_name)).isoformat() \
                and self.modified == datetime.fromtimestamp(getmtime(qual_name)).isoformat())

    def hash_matches(self, qual_name: str) -> bool:
        hasher = hashlib.md5()
        with open(qual_name, 'rb') as afile:
            hasher.update(afile.read())
            digest = hasher.hexdigest()
            logger.debug('comparing file hash: %s with index: %s',
                           digest, self.hash)
            return compare_digest(self.hash.strip(), digest.strip())

    @model_serializer
    def ser_model(self) -> str:
        return f'{quote(self.name)},{self.created},{self.modified},{self.size},{self.hash}\n'
