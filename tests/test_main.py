import pytest
import pytest_check
from pytest_mock import mocker
from main import main

def test_specific_target(mocker):
    # mock the 'run' function of main for now
    # fill out the run functionality later and then mock
    # the slow parts of the Component class
    mocker.patch('main.run_session', return_value=False)
    assert main(["Vimeo"]) == 0

def test_multi_inputs():
    assert main(["Vimeo", "concrete5"]) == 0

def test_all_targets():
    assert main(["AllAvailableTargets"]) == 0

def test_missing_target():
    assert main(["test.com"]) == 0

def test_search_target():
    assert main(["Monocle", "-s"])[0] == "Big Monocle"

def test_reverse_args():
    assert main(["-s", "Monocle"])[0] == "Big Monocle"

