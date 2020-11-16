import pytest_check
from main import main

def test_multi_inputs():
    assert main(["example.com", "test.com"]) == 0

def test_no_input():
    assert main([""]) == 0