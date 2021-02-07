import json
import pytest_check as check
from pytest_mock import mocker
from pathlib import Path
from components.getsubdomains import GetSubdomains

def test_install_getsubdomains():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    assert mod.install() == 0

def test_input():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    for each in mod.input:
        check.is_true( Path(mod.session_path / each).exists() )

def test_getsubdomains_amass():
    # This test takes a looong time to run
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    result = mod.amass("example.com")
    assert result == 0

def test_getsubdomains_bass():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    result = mod.bass("example.com")
    assert result == 0

def test_getsubdomains_subfinder():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    result = mod.subfinder("example.com")
    assert result == 0

def test_getsubdomains_hakrawler():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    result = mod.hakrawler("example.com")
    assert result == 0

def test_getsubdomains_resolve():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    mod.all_subdomains = ["test.example.com", "test2.example.com", "test3.example.com"]
    result = mod.resolve_all()
    assert result == 0

def test_getsubdomains_subscraper():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    result = mod.subscraper("example.com")
    assert result == 0

def test_check_scope_negative():
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    result = mod.check_scope("mapi.example.com", "example").decode('utf-8')
    check.is_not_in("mapi.example.com", result)

def test_check_scope_postive():
    _session_path = "assets/example.com/test"
    resultdir = Path.home() / _session_path
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, _session_path)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
    # Check for existing instances or create a small fleet
    mod.axiom.select(mod.axiom_name)
    if len(mod.axiom.instances) == 0:
        mod.axiom.fleet(1)
    # Run the tool
    results = mod.exec_tool(mod.check_scope, 1, "api.example.com", "example")
    # Check the results
    check.is_not([], results)
    for r in results:
        check.is_in("api.example.com", r)

def test_run_getsubdomains(mocker):
    # mock the methods that run tools to just test the "run" functionality
    resultdir = Path.home() / "assets" / "example.com" / "test"
    resultdir.mkdir(parents=True, exist_ok=True)
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
    # Save scope as a file
    scopef = resultdir / f"scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    mod = GetSubdomains("example", scopef, resultdir)
    # Save primary domains list
    with open(resultdir / mod.input[0], "w+") as f:
        f.write("example.com")
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
    result = mod.run()
    assert result == 0
