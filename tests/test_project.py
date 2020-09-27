import pytest
from project import Project

def test_project():
    project1 = Project()
    assert project1

print("Name: " + __name__)
test_project()