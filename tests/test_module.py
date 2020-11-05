import pytest_check as check
from pathlib import Path
from module import Module
from modules.getsubdomains import GetSubdomains

def test_module_runfile_exists():
    scope = Path.home() / 'targets' / 'example.com.json'
    with open(scope, 'w+') as fs:
        fs.write('{example.com}')
    mod = GetSubdomains("example.com", scope)
    check.is_true( Path(mod.modfile).exists() )

def test_install():
    scope = Path.home() / 'targets' / 'example.com.json'
    with open(scope, 'w+') as fs:
        fs.write('{example.com}')
    mod = GetSubdomains("example.com", scope)
    # False here means a good result, any other result is error
    check.is_false(mod.install())

def test_input():
    scope = Path.home() / 'targets' / 'example.com.json'
    with open(scope, 'w+') as fs:
        fs.write('{example.com}')
    mod = GetSubdomains("example.com", scope)
    for each in mod.input:
        check.is_true( Path(each).exists() )

def test_run_getsubdomains():
    scope = Path.home() / 'targets' / 'example.com.json'
    with open(scope, 'w+') as fs:
        fs.write('{example.com}')
    mod = GetSubdomains("example.com", scope)
    check.is_not_none(mod.run())
