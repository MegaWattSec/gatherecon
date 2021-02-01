import pytest_check as check
from pytest_mock import mocker
from axiom import Axiom

def test_get_all_instances():
    axiom = Axiom()
    axiom.name = "test"
    instances = axiom.get_all_instances()
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    check.greater(len(instances), 0)

def test_selected_instances():
    axiom = Axiom()
    axiom.name = "test"
    axiom.select_instances()
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    check.greater(len(axiom.instances), 0)

def test_exec():
    axiom = Axiom()
    axiom.name = "test"
    axiom.select_instances()
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    results = axiom.exec("whoami")
    print(results)
    check.is_not_none(results)
    check.is_not_in("Connection refused", results)

def test_fleet():
    axiom = Axiom()
    axiom.name = "test"
    axiom.select_instances()
    results = axiom.fleet(2)
    print(results)
    check.is_in("Fleet started succesfully!", results)

def test_remove():
    axiom = Axiom()
    axiom.name = "test"
    axiom.select_instances()
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    selection = axiom.select_instances()
    for each in selection:
        result = axiom.remove(each)
        check.is_in(f"Deleting {each}", result)