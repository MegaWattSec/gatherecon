import pytest_check as check
from pathlib import Path
from module import Module

def test_tool_path():
    mod = Module("modules/get_subdomains.sh")
    check.is_true( Path(mod.module).exists() )

def test_install_check():
    mod = Module("modules/get_subdomains.sh")
    # False here means a good result, any other result is error
    check.is_false(mod.check())

# def test_required_input():


# def test_output_path():


# def test_input_check():


# def test_run():


# def test_clean_assets():


# def test_asset_db_save():
