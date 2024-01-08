"""
suite testing models
"""
import logging

import pytest
from pydantic import BaseModel

from imagectl.models import IndexEntry

ENTRY = 'foo,2024-01-01T10:30:00,2024-01-01T10:30:00,1024,\n'
ENTRY_WITH_COMMA_IN_NAME = 'foo%2Cbar,2024-01-01T10:30:00,2024-01-01T10:30:00,1024,\n'
# @pytest.fixture(scope="session")
# def github():
#     """ initialise a GitHubReader instance """
#     logging.basicConfig() #NOSONAR
#     logger.setLevel(args.verbose)
#     options = {
#         'verbose': "DEBUG"
#     }
#     reader = GitHubReader(GitHubReaderOptions(**options))
#     assert reader is not None
#     return reader

def test_serialise():
    """test csv serialisation"""
    entry = IndexEntry(name="foo",
                       created="2024-01-01T10:30:00",
                       modified="2024-01-01T10:30:00",
		       size=1024)
    str = entry.model_dump()
    assert str == ENTRY

    entry.name = 'foo,bar'
    str = entry.model_dump()
    assert str == ENTRY_WITH_COMMA_IN_NAME

def test_deserialise():
    """test csv deserialisation"""
    entry = IndexEntry.from_str(ENTRY)
    assert entry.name == 'foo'
    assert entry.created == "2024-01-01T10:30:00"
    assert entry.modified == "2024-01-01T10:30:00"

    entry = IndexEntry.from_str(ENTRY_WITH_COMMA_IN_NAME)
    assert entry.name == 'foo,bar'
    assert entry.created == "2024-01-01T10:30:00"
    assert entry.modified == "2024-01-01T10:30:00"
    assert entry.size == 1024
    assert entry.size == 1024