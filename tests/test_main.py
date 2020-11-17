import pytest
import pytest_check
from main import main

def test_specific_target():
    assert main(["Vimeo"]) == 0

def test_multi_inputs():
    assert main(["Vimeo", "concrete5"]) == 0

def test_all_targets():
    assert main(["AllAvailableTargets"]) == 0

def test_missing_target():
    assert main(["test.com"]) == 0