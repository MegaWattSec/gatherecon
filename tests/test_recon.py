import random
import pytest
import pymongo
from pathlib import Path
from datetime import datetime
from recon import ReconSession, SessionList

def test_session_date():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession(tdomain, tscope)
    assert isinstance(tsession.date, datetime)

# Test for a successful MongoDb connection
def test_database():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession(tdomain, tscope)
    assert tsession._client

# Test that recon session path is a valid directory
def test_path():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession(tdomain, tscope)
    assert Path(tsession.path).exists()

# Test for the session by returned ID
def test_session_id():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession(tdomain, tscope)
    print("\n\nSession ID: " + tsession.id)
    assert tsession.id

# Test that scope is being saved in the database
def test_session_scope():
    tdomain = "example.com"
    tscope = random.randrange(1, 100000)
    tsession = ReconSession(tdomain, tscope)
    with tsession as ts:
        print("\n\nDocument: " + str(ts.db_document))
        assert ts.db_document["scope"] == tscope

# Test for recon session modules list
def test_modules_list():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession(tdomain, tscope)
    assert tsession.modules

# Test for session list
def test_session_list():
    tdomain = "example.com"
    tscope = "*.example.com"
    # create an unused session to have at least 1 in the list
    ReconSession(tdomain, tscope)
    tlist = SessionList(tdomain)
    assert tlist.get_count() >= 1

# Test the session compare method
def test_compare():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession(tdomain, tscope)
    with SessionList(tdomain) as slist:
        srecent = slist.get_previous()
        if srecent:
            assert not tsession.compare(srecent[0])
        else:
            assert False
