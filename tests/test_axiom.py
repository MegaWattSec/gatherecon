import time
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
    axiom.select("test")
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    check.greater(len(axiom.instances), 0)

def test_exec():
    axiom = Axiom()
    axiom.select("test")
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    results = axiom.exec("whoami")
    print(results)
    check.is_not_none(results)
    check.is_not_in("Connection refused", results)

def test_fleet():
    axiom = Axiom()
    axiom.select("test")
    results = axiom.fleet(2)
    print(results)
    check.is_in("Fleet started succesfully!", results)

def test_remove():
    axiom = Axiom()
    axiom.select("test")
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    for each in axiom.instances:
        print(each)
        axiom.remove(each)
    time.sleep(10)
    result = axiom.select("test")
    print(result)
    assert result == []

def test_send_file(tmp_path):
    axiom = Axiom()
    axiom.select("test")
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    testfile = tmp_path / "testfile.txt"
    # Need to write file and put it on fleet to copy from later
    with open(testfile, "w+") as f:
        f.write("THis is a test file.")
    result = axiom.send(testfile, "testfile.txt", axiom.instances[0])
    assert "rsync error" not in result
    assert "ERROR" not in result

def test_get_file(tmp_path):
    axiom = Axiom()
    axiom.select("test")
    if len(axiom.instances) == 0:
        axiom.fleet(1)
    testfile = tmp_path / "testfile.txt"
    # Need to write file and put it on fleet to copy from later
    with open(testfile, "w+") as f:
        f.write("THis is a test file.")
    result = axiom.send(testfile, "testfile.txt", axiom.instances[0])
    # check.is_not_in("rsync error", result, "Could not get test file to instance.")
    assert "rsync error" not in result
    assert "ERROR" not in result
    # Copy file from fleet and save as a different name.
    test_receive = tmp_path / "test_received.txt"
    result = axiom.get("testfile.txt", test_receive, axiom.instances[0])
    assert "rsync error" not in result
    assert "ERROR" not in result
    assert test_receive.read_text() == "THis is a test file."
    assert len(list(tmp_path.iterdir())) == 2