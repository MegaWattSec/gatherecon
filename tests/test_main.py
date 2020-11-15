import pytest_check
from main import main

def test_main():
    pytest_check.is_false( main() )