import pytest
from ghostlink.hardware_utils import is_admin, is_virtual_machine, list_physical_nics


def test_is_virtual_machine_returns_bool():
    val = is_virtual_machine()
    assert isinstance(val, bool)


def test_is_admin_returns_bool():
    val = is_admin()
    assert isinstance(val, bool)


def test_list_nics_returns_list():
    nics = list_physical_nics()
    assert isinstance(nics, list)
