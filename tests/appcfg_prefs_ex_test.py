import pytest
from gfixture import NC_APP

from nc_py_api import NextcloudExceptionNotFound

if NC_APP is None or "app_ecosystem_v2" not in NC_APP.capabilities:
    pytest.skip("app_ecosystem_v2 is not installed.", allow_module_level=True)


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_get_value_invalid(class_to_test):
    with pytest.raises(ValueError):
        class_to_test.get_value("")


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_get_values_invalid(class_to_test):
    assert class_to_test.get_values([]) == []
    with pytest.raises(ValueError):
        class_to_test.get_values([""])
    with pytest.raises(ValueError):
        class_to_test.get_values(["", "k"])


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_set_empty_key(class_to_test):
    with pytest.raises(ValueError):
        class_to_test.set_value("", "some value")


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_delete_invalid(class_to_test):
    class_to_test.delete([])
    with pytest.raises(ValueError):
        class_to_test.delete([""])
    with pytest.raises(ValueError):
        class_to_test.delete(["", "k"])


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_get_default(class_to_test):
    assert class_to_test.get_value("non_existing_key", default="alice") == "alice"


@pytest.mark.parametrize("value", ("0", "1", "12 3", ""))
@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_set_delete(value, class_to_test):
    class_to_test.delete("test_key")
    assert class_to_test.get_value("test_key") is None
    class_to_test.set_value("test_key", value)
    assert class_to_test.get_value("test_key") == value
    class_to_test.set_value("test_key", "zzz")
    assert class_to_test.get_value("test_key") == "zzz"
    class_to_test.delete("test_key")
    assert class_to_test.get_value("test_key") is None


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_delete(class_to_test):
    class_to_test.set_value("test_key", "123")
    assert class_to_test.get_value("test_key")
    class_to_test.delete("test_key")
    assert class_to_test.get_value("test_key") is None
    class_to_test.delete("test_key")
    class_to_test.delete(["test_key"])
    with pytest.raises(NextcloudExceptionNotFound):
        class_to_test.delete("test_key", not_fail=False)
    with pytest.raises(NextcloudExceptionNotFound):
        class_to_test.delete(["test_key"], not_fail=False)


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_get(class_to_test):
    class_to_test.delete(["test key", "test key2"])
    assert len(class_to_test.get_values(["test key", "test key2"])) == 0
    class_to_test.set_value("test key", "123")
    assert len(class_to_test.get_values(["test key", "test key2"])) == 1
    class_to_test.set_value("test key2", "123")
    assert len(class_to_test.get_values(["test key", "test key2"])) == 2


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_multiply_delete(class_to_test):
    class_to_test.set_value("test_key", "123")
    class_to_test.set_value("test_key2", "123")
    assert len(class_to_test.get_values(["test_key", "test_key2"])) == 2
    class_to_test.delete(["test_key", "test_key2"])
    assert len(class_to_test.get_values(["test_key", "test_key2"])) == 0
    class_to_test.delete(["test_key", "test_key2"])
    class_to_test.set_value("test_key", "123")
    assert len(class_to_test.get_values(["test_key", "test_key2"])) == 1
    class_to_test.delete(["test_key", "test_key2"])
    assert len(class_to_test.get_values(["test_key", "test_key2"])) == 0


@pytest.mark.parametrize("key", ("k", "k y", " "))
@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_get_non_existing(key, class_to_test):
    class_to_test.delete(key)
    assert class_to_test.get_value(key) is None
    assert class_to_test.get_values([key]) == []
    assert len(class_to_test.get_values([key, "non_existing_key"])) == 0


@pytest.mark.parametrize("class_to_test", (NC_APP.appconfig_ex, NC_APP.preferences_ex))
def test_cfg_ex_get_typing(class_to_test):
    class_to_test.set_value("test key", "123")
    class_to_test.set_value("test key2", "321")
    r = class_to_test.get_values(["test key", "test key2"])
    assert isinstance(r, list)
    assert r[0].key == "test key"
    assert r[1].key == "test key2"
    assert r[0].value == "123"
    assert r[1].value == "321"


def test_appcfg_sensitive():
    appcfg = NC_APP.appconfig_ex
    appcfg.delete("test_key")
    appcfg.set_value("test_key", "123", sensitive=True)
    assert appcfg.get_value("test_key") == "123"
    assert appcfg.get_values(["test_key"])[0].value == "123"
    appcfg.delete("test_key")
    # next code tests `sensitive` value from the `AppEcosystem`
    params = {"configKey": "test_key", "configValue": "123"}
    result = NC_APP._session.ocs(method="POST", path=f"{NC_APP._session.ae_url}/{appcfg._url_suffix}", json=params)
    assert not result["sensitive"]  # by default if sensitive value is unspecified it is False
    appcfg.delete("test_key")
    params = {"configKey": "test_key", "configValue": "123", "sensitive": True}
    result = NC_APP._session.ocs(method="POST", path=f"{NC_APP._session.ae_url}/{appcfg._url_suffix}", json=params)
    assert result["configkey"] == "test_key"
    assert result["configvalue"] == "123"
    assert bool(result["sensitive"]) is True
    params.pop("sensitive")  # if we not specify value, AppEcosystem should not change it.
    result = NC_APP._session.ocs(method="POST", path=f"{NC_APP._session.ae_url}/{appcfg._url_suffix}", json=params)
    assert result["configkey"] == "test_key"
    assert result["configvalue"] == "123"
    assert bool(result["sensitive"]) is True
    params["sensitive"] = False
    result = NC_APP._session.ocs(method="POST", path=f"{NC_APP._session.ae_url}/{appcfg._url_suffix}", json=params)
    assert result["configkey"] == "test_key"
    assert result["configvalue"] == "123"
    assert bool(result["sensitive"]) is False
