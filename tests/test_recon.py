import random
import pytest_check as check
import pymongo
from pathlib import Path
from datetime import datetime
from recon import ReconSession
from config import Config

# Test a config file update
def test_config():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession(ttarget, tscope)
    assert trecon._db.name == "test"
    tconfig.db_name = db_old

# Test for a successful MongoDb connection
def test_database():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession(ttarget, tscope)
    assert trecon._client
    tconfig.db_name = db_old

# Test for session list count
def test_session_count():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    tsessions = ReconSession(ttarget, tscope)
    assert tsessions.get_count() >= 1
    tconfig.db_name = db_old

# Test get all sessions
def test_sessions_list():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    tsessions = ReconSession(ttarget, tscope)
    assert isinstance(tsessions.get_sessions(), pymongo.cursor.Cursor)
    tconfig.db_name = db_old

# Test for latest session
def test_latest_session():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    tsessions = ReconSession(ttarget, tscope)
    assert isinstance(tsessions.get_latest(), pymongo.cursor.Cursor)
    tconfig.db_name = db_old

# test for previous session
def test_previous_session():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    tsessions = ReconSession(ttarget, tscope)
    assert isinstance(tsessions.get_previous(), pymongo.cursor.Cursor)
    tconfig.db_name = db_old

def test_recon_date():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession(ttarget, tscope)
    assert isinstance(trecon.date, datetime)
    tconfig.db_name = db_old

# Test that recon session path is a valid directory
def test_path():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession(ttarget, tscope)
    assert Path(trecon.path).exists()
    tconfig.db_name = db_old

# Test for the session by returned ID
def test_recon_id():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession(ttarget, tscope)
    assert trecon.id
    tconfig.db_name = db_old

# Test that scope is being saved in the database
def test_recon_scope():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = random.randrange(1, 100000)
    trecon = ReconSession(ttarget, tscope)
    with trecon as ts:
        assert ts.db_document["scope"] == tscope
    tconfig.db_name = db_old

# Test for recon session components list
def test_components_check():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession(ttarget, tscope)
    print(trecon.component_list)
    if not trecon.component_list:
        assert False
    for mod in trecon.component_list:
        assert trecon.check_component(mod)
    tconfig.db_name = db_old

# Test for the Target collection
def test_target_collection():
    tconfig = Config()
    db_old = tconfig.db_name
    tconfig.db_name = "test"
    ttarget = "example.com"
    tscope = "*.example.com"
    trecon = ReconSession(ttarget, tscope)
    assert trecon._db.Targets.count_documents({}) >= 1
    tconfig.db_name = db_old