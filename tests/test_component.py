import pytest_check as check
from pathlib import Path
from components.getsubdomains import GetSubdomains

def test_component_runfile_exists():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    scope = {
        "target": {
            "scope": {
                "advanced_mode": 'true',
                "exclude": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^.*\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ],
                "include": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^api\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ]
            }
        }
    }
    mod = GetSubdomains("example.com", scope, resultdir)
    check.is_true( Path(mod.modfile).exists() )

def test_install():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    scope = {
        "target": {
            "scope": {
                "advanced_mode": 'true',
                "exclude": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^.*\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ],
                "include": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^api\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ]
            }
        }
    }
    mod = GetSubdomains("example.com", scope, resultdir)
    # False here means a good result, any other result is error
    check.is_false(mod.install())

def test_input():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    scope = {
        "target": {
            "scope": {
                "advanced_mode": 'true',
                "exclude": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^.*\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ],
                "include": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^api\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ]
            }
        }
    }
    mod = GetSubdomains("example.com", scope, resultdir)
    for each in mod.input:
        check.is_true( Path(each).exists() )

def test_install_getsubdomains():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    scope = {
        "target": {
            "scope": {
                "advanced_mode": 'true',
                "exclude": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^.*\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ],
                "include": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^api\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ]
            }
        }
    }
    mod = GetSubdomains("example.com", scope, resultdir)
    check.is_false(mod.install())    # false here is a good result

def test_run_getsubdomains():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    scope = {
        "target": {
            "scope": {
                "advanced_mode": 'true',
                "exclude": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^.*\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ],
                "include": [
                    {
                        "enabled": 'true',
                        "file": "^/.*",
                        "host": "^api\\.example\\.com$",
                        "port": "^80$",
                        "protocol": "http"
                    },
                ]
            }
        }
    }
    mod = GetSubdomains("example.com", scope, resultdir)
    check.is_not_none(mod.run())
