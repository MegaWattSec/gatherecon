import pytest
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

def test_name():
    cfg = Config()
    assert isinstance(cfg.db_name, str)

def test_modules():
    cfg = Config()
    print("\n\nModules available: ")
    for mod in cfg.modules:
        print(mod)
    assert isinstance(cfg.modules, list)
