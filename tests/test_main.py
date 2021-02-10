import json
import pytest_check
from pytest_mock import mocker
from pathlib import Path
from main import main, create_graph, run_session

def test_specific_target(mocker):
    # mock the 'run' function of main for now
    # fill out the run functionality later and then mock
    # the slow parts of the Component class
    mocker.patch(
        "main.run_session",
        return_value=0
    )
    assert main(["vimeo"]) == 0

def test_multi_inputs(mocker):
    # Mock run_session to return a good result
    mocker.patch(
        "main.run_session",
        return_value=0
    )
    assert main(["vimeo", "concrete5"]) == 0

def test_all_targets(mocker):
    # Mock run_session to return a good result
    mocker.patch(
        "main.run_session",
        return_value=0
    )

    # Execute against all available targets
    assert main(["AllAvailableTargets"]) == 0

def test_missing_target(mocker):
    # Mock run_session to return a good result
    mocker.patch(
        "main.run_session",
        return_value=0
    )

    assert main(["thistargetshouldnotexist.com"]) == 0

def test_search():
    # should return a list of dictionaries (one in this case)
    res = [ each['name'] for each in main(["Monocle", "-s"]) ]
    assert "Big Monocle" in res

def test_search_reverse_args():
    # should return a list of dictionaries (one in this case)
    res = [ each['name'] for each in main(["Monocle", "-s"]) ]
    assert "Big Monocle" in res

def test_search_multi_targets():
    # should return a list of dictionaries
    # Test the length of the return to be greater than 1
    #assert len(main(["-s", "A"])) > 1
    res = [ each['name'] for each in main(["A", "-s"]) ]
    assert "Acronis" and "Adobe" in res

def test_search_alltargets():
    # should return a list of all targets (over 400 of them)
    assert len(main(["AllAvailableTargets", "-s"])) > 400

def test_search_missing():
    # should return an empty list
    assert main(["thistargetshouldnotexist.com", "-s"]) == []

def test_update_scopes():
    # results show how many scopes were updates/added
    # zero means no scopes were affected
    # -1 means there was an error
    assert main(["-u"]) >= 0

def test_create_graph():
    # test by creating a graph from a component test directory
    levl = create_graph("tests.components")
    # Check how many component levels are returned
    pytest_check.check( len(levl) == 1 )
    # Check how many components in the level
    pytest_check.check( len(levl[0]) == 2 )

def test_run_session():
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
    scopef = resultdir / "scope.json"
    with open(scopef, "w+") as f:
        f.write(f"[{json.dumps(scope)}]")
    # Save domain list for GetSubdomains
    domainf = resultdir / "primary_domains.txt"
    with open(domainf, "w+") as f:
        f.write("example.com")
    results = run_session("api.example.com", scopef, "database", "session", resultdir)
    assert results == [0]
    with open(resultdir / "subs" / "active_subs.txt", "r") as f:
        assert "www.example.com" in f.read()