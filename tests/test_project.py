import pytest
from project import Project
from recon import ReconSession
from gatherdb import GatherDb, SessionList
from probe import Probe

def test_instantiation_exists():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert tproject

def test_current_recon_session_exists():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    tproject.start_recon()
    assert tproject.current_recon

def test_database_exists():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert tproject.db

def test_probe_session_exists():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert tproject.start_probe()

def test_list_recon_exists():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert tproject.list_recon()

def test_schedule_recon_exists():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert tproject.schedule_recon()

def test_compare_recon_exists():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert tproject.compare_recon()

def test_domain_type():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert isinstance(tproject.domain, str)

def test_current_recon_session_type():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    tproject.start_recon()
    assert isinstance(tproject.current_recon, ReconSession)

def test_database_type():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    assert isinstance(tproject.db, GatherreconDb)

def test_probe_session_type():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    tprobe = tproject.start_probe()
    assert isinstance(tprobe, Probe)

def test_list_recon_type():
    tdomain = "example.com"
    tscope = "*.example.com"
    tproject = Project(tdomain, tscope)
    treconlist = tproject.list_recon()
    assert isinstance(treconlist, SessionList)

