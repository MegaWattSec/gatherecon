import pytest_check as check
from config import Config
from pathlib import Path

def test_config_file():
    cfg = Config()
    assert Path(cfg.configfile).exists()

def test_host():
    cfg = Config()
    assert isinstance(cfg.db_host, str)

def test_host_change():
    cfg = Config()
    host_old = cfg.db_host
    cfg.db_host = "testhoststring"
    check.equal(cfg.db_host, "testhoststring")
    cfg.db_host = host_old

def test_name():
    cfg = Config()
    assert isinstance(cfg.db_name, str)

def test_name_change():
    cfg = Config()
    name_old = cfg.db_name
    cfg.db_name = "testnamestring"
    check.equal(cfg.db_name, "testnamestring")
    cfg.db_name = name_old

def test_modules():
    cfg = Config()
    print("\n\nModules available: ")
    print(cfg.modules)
    assert isinstance(cfg.modules, list)
