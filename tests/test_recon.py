import random
import pytest
import pymongo
from pathlib import Path
from datetime import datetime
from recon import ReconSession, SessionList

def test_session_date():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession("test", tdomain, tscope)
    assert isinstance(tsession.date, datetime)
    tsession._db.Domains.remove({})
    tsession._db.Sessions.remove({})

# Test for a successful MongoDb connection
def test_database():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession("test", tdomain, tscope)
    assert tsession._client
    tsession._db.Domains.remove({})
    tsession._db.Sessions.remove({})

# Test that recon session path is a valid directory
def test_path():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession("test", tdomain, tscope)
    assert Path(tsession.path).exists()
    tsession._db.Domains.remove({})
    tsession._db.Sessions.remove({})

# Test for the session by returned ID
def test_session_id():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession("test", tdomain, tscope)
    print("\n\nSession ID: " + tsession.id)
    assert tsession.id
    tsession._db.Domains.remove({})
    tsession._db.Sessions.remove({})

# Test that scope is being saved in the database
def test_session_scope():
    tdomain = "example.com"
    tscope = random.randrange(1, 100000)
    tsession = ReconSession("test", tdomain, tscope)
    with tsession as ts:
        print("\n\nDocument: " + str(ts.db_document))
        assert ts.db_document["scope"] == tscope
        tsession._db.Domains.remove({})
        tsession._db.Sessions.remove({})

# Test for recon session modules list
def test_modules_list():
    tdomain = "example.com"
    tscope = "*.example.com"
    tsession = ReconSession("test", tdomain, tscope)
    assert tsession.modules
    tsession._db.Domains.remove({})
    tsession._db.Sessions.remove({})

# Test for session list count
def test_session_list():
    tdomain = "example.com"
    tscope = "*.example.com"
    # create an unused session to have at least 1 in the list
    ReconSession("test", tdomain, tscope)
    tsessions = SessionList("test", tdomain)
    assert tsessions.get_count() >= 1
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

# Test the session compare method
def test_compare():
    tdomain = "example.com"
    tscope = "*.example.com"
    ReconSession("test", tdomain, tscope)
    tsession = ReconSession("test", tdomain, tscope)
    with SessionList("test", tdomain) as slist:
        srecent = slist.get_previous()
        if srecent:
            assert not tsession.compare(srecent[0])
        else:
            assert False
        tsession._db.Domains.remove({})
        tsession._db.Sessions.remove({})
