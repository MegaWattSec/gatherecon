import random
import pytest
import pymongo
from pathlib import Path
from datetime import datetime
from recon import ReconSession, SessionList

# Test for session list count
def test_session_count():
    tdomain = "example.com"
    tscope = "*.example.com"
    # create an unused session to have at least 1 in the list
    ReconSession("test", tdomain, tscope)
    tsessions = SessionList("test", tdomain)
    assert tsessions.get_count() >= 1
    tsessions._db.Domains.remove({})
    tsessions._db.Sessions.remove({})

# Test get all sessions
def test_sessions_list():
    tdomain = "example.com"
    tscope = "*.example.com"
    # create an unused session to have at least 1 in the list
    ReconSession("test", tdomain, tscope)
    tsessions = SessionList("test", tdomain)
    assert isinstance(tsessions.get_sessions(), pymongo.cursor.Cursor)
    tsessions._db.Domains.remove({})
    tsessions._db.Sessions.remove({})

# Test for latest session
def test_latest_session():
    tdomain = "example.com"
    tscope = "*.example.com"
    # create an unused session to have at least 1 in the list
    ReconSession("test", tdomain, tscope)
    tsessions = SessionList("test", tdomain)
    assert isinstance(tsessions.get_latest(), pymongo.cursor.Cursor)
    tsessions._db.Domains.remove({})
    tsessions._db.Sessions.remove({})

# test for previous session
def test_previous_session():
    tdomain = "example.com"
    tscope = "*.example.com"
    # create an unused session to have at least 1 in the list
    ReconSession("test", tdomain, tscope)
    tsessions = SessionList("test", tdomain)
    assert isinstance(tsessions.get_previous(), pymongo.cursor.Cursor)
    tsessions._db.Domains.remove({})
    tsessions._db.Sessions.remove({})

def test_recon_date():
    tdomain = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession("test", tdomain, tscope)
    assert isinstance(trecon.date, datetime)
    trecon._db.Domains.remove({})
    trecon._db.Sessions.remove({})

# Test for a successful MongoDb connection
def test_database():
    tdomain = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession("test", tdomain, tscope)
    assert trecon._client
    trecon._db.Domains.remove({})
    trecon._db.Sessions.remove({})

# Test that recon session path is a valid directory
def test_path():
    tdomain = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession("test", tdomain, tscope)
    assert Path(trecon.path).exists()
    trecon._db.Domains.remove({})
    trecon._db.Sessions.remove({})

# Test for the session by returned ID
def test_recon_id():
    tdomain = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession("test", tdomain, tscope)
    assert trecon.id
    trecon._db.Domains.remove({})
    trecon._db.Sessions.remove({})

# Test that scope is being saved in the database
def test_recon_scope():
    tdomain = "example.com"
    tscope = random.randrange(1, 100000)
    trecon = ReconSession("test", tdomain, tscope)
    with trecon as ts:
        assert ts.db_document["scope"] == tscope
        trecon._db.Domains.remove({})
        trecon._db.Sessions.remove({})

# Test for recon session modules list
def test_modules_list():
    tdomain = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession("test", tdomain, tscope)
    assert trecon.modules
    trecon._db.Domains.remove({})
    trecon._db.Sessions.remove({})

# Test the compare method
def test_compare():
    tdomain = "example.com"
    tscope = "*.example.com"
    ReconSession("test", tdomain, tscope)
    trecon = ReconSession("test", tdomain, tscope)
    with SessionList("test", tdomain) as slist:
        srecent = slist.get_previous()
        if srecent:
            assert not trecon.compare(srecent[0])
        else:
            assert False
        trecon._db.Domains.remove({})
        trecon._db.Sessions.remove({})
