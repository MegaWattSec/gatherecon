import pytest
import pytest_check as check
import random
from config import Config
from pathlib import Path
from box import BoxError, BoxList

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
    for mod in cfg.modules:
        print(mod)
    assert isinstance(cfg.modules, list)

def test_modules_change():
    cfg = Config()
    modules_old = cfg.modules
    cfg.modules = ["testmodulesstring"]
    check.equal(cfg.modules, ["testmodulesstring"])
    cfg.modules = modules_old
