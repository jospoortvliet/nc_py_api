import pytest
from gfixture import NC_TO_TEST

from nc_py_api import NextcloudException


@pytest.mark.parametrize("nc", NC_TO_TEST)
def test_available(nc):
    assert isinstance(nc.preferences.available, bool)


@pytest.mark.parametrize("nc", NC_TO_TEST)
def test_preferences_set(nc):
    if not nc.preferences.available:
        pytest.skip("provisioning_api is not available")
    nc.preferences.set_value("dav", key="user_status_automation", value="yes")
    with pytest.raises(NextcloudException):
        nc.preferences.set_value("non_existing_app", "some_cfg_name", "2")


@pytest.mark.parametrize("nc", NC_TO_TEST)
def test_preferences_delete(nc):
    if not nc.preferences.available:
        pytest.skip("provisioning_api is not available")
    nc.preferences.delete("dav", key="user_status_automation")
    with pytest.raises(NextcloudException):
        nc.preferences.delete("non_existing_app", "some_cfg_name")
