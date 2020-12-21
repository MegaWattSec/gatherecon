import pytest_check
from pytest_mock import mocker
from main import main, create_graph

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

def test_missing_target():
    # Mock run_session to return a good result
    mocker.patch(
        "main.run_session",
        return_value=0
    )

    assert main(["thistargetshouldnotexist.com"]) == 0

def test_search():
    # should return a list of strings (one in this case)
    assert main(["Monocle", "-s"])[0] == "Big Monocle"

def test_search_reverse_args():
    # should return a list of strings (one in this case)
    assert main(["-s", "Monocle"]) == ["Big Monocle"]

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

    assert True