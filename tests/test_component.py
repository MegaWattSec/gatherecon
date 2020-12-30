import pytest_check as check
from pathlib import Path
from components.getsubdomains import GetSubdomains

def test_component_runfile_exists():
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
    mod = GetSubdomains("example.com", scope)
    check.is_true( Path(mod.modfile).exists() )

def test_install():
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
    mod = GetSubdomains("example.com", scope)
    # False here means a good result, any other result is error
    check.is_false(mod.install())

def test_input():
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
    mod = GetSubdomains("example.com", scope)
    for each in mod.input:
        check.is_true( Path(each).exists() )

def test_run_getsubdomains():
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
    mod = GetSubdomains("example.com", scope)
    check.is_not_none(mod.run())
