import pytest_check as check
from pytest_mock import mocker
from pathlib import Path
from components.getsubdomains import GetSubdomains

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

def test_getsubdomains_amass():
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
    result = mod.amass()
    check.is_false(result)

def test_getsubdomains_bass():
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
    result = mod.bass()
    check.is_false(result)

def test_getsubdomains_subfinder():
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
    result = mod.subfinder()
    check.is_false(result)

def test_getsubdomains_hakrawler():
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
    result = mod.hakrawler()
    check.is_false(result)

def test_getsubdomains_resolve():
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
    mod.all_subdomains = ["test.example.com", "test2.example.com", "test3.example.com"]
    result = mod.resolve_all()
    check.is_false(result)

def test_getsubdomains_subscraper():
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
    result = mod.subscraper()
    check.is_false(result)

def test_check_scope_negative():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    scope = {
        "handle": "example",
            "targets": {
                "out_of_scope": [
                    {
                        "asset_identifier": "*.example.com"
                    },
                ],
                "in_scope": [
                    {
                        "asset_identifier": "api.example.com"
                    },
                ]
            }
    }
    mod = GetSubdomains("example.com", scope, resultdir)
    result = mod.check_scope("mapi.example.com", "example").decode('utf-8')
    check.is_not_in("mapi.example.com", result)

def test_check_scope_postive():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    scope = {
        "handle": "example",
            "targets": {
                "out_of_scope": [
                    {
                        "asset_identifier": "*.example.com"
                    },
                ],
                "in_scope": [
                    {
                        "asset_identifier": "api.example.com"
                    },
                ]
            }
    }
    mod = GetSubdomains("example.com", scope, resultdir)
    result = mod.check_scope("api.example.com", "example").decode('utf-8')
    check.is_not("", result)
    check.is_in("api.example.com", result)

def test_run_getsubdomains(mocker):
    # mock the methods that run tools to just test the "run" functionality
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
    mocker.patch(
        "components.getsubdomains.GetSubdomains.bass",
        return_value=0
    )
    mocker.patch(
        "components.getsubdomains.GetSubdomains.subfinder",
        return_value=0
    )
    mocker.patch(
        "components.getsubdomains.GetSubdomains.amass",
        return_value=0
    )
    mocker.patch(
        "components.getsubdomains.GetSubdomains.hakrawler",
        return_value=0
    )
    mocker.patch(
        "components.getsubdomains.GetSubdomains.subscraper",
        return_value=0
    )
    mod = GetSubdomains("example.com", scope, resultdir)
    result = mod.run()
    check.is_false(result)
