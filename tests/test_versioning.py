import pytest
from _pytest.capture import CaptureFixture
from pytest_mock import MockerFixture

from pylib.common import get_pyproject

from pylib.semver import VersionInfo
from pylib.assert_prod_version import assert_prod_version
from pylib.assert_version_available import assert_version_available
from pylib.set_next_dev_version import set_next_dev_version


PYPROJECT_TOML_WITH_PROD_VERSION = b"""
[tool.poetry]
name = "rtb-apps-dev"
version = "0.1.0"
description = "RTB House Apps rtb-apps-dev"
authors = ["RTB House Apps Team <apps@rtbhouse.com>"]
"""


PYPROJECT_TOML_WITH_DEV_VERSION = b"""
[tool.poetry]
name = "rtb-apps-dev"
version = "0.1.0-dev.0"
description = "RTB House Apps rtb-apps-dev"
authors = ["RTB House Apps Team <apps@rtbhouse.com>"]
"""


VERSIONS_AVAILABLE_WITH_VERSION_AVAILABLE = [
    VersionInfo(0, 0, 1),
    VersionInfo(0, 0, 3),
    VersionInfo(0, 0, 8),
]


VERSIONS_AVAILABLE_WITH_VERSION_NOT_AVAILABLE = [
    *VERSIONS_AVAILABLE_WITH_VERSION_AVAILABLE,
    VersionInfo(0, 1, 0),
]


DEV_VERSIONS = [
    VersionInfo(0, 1, 0, "dev1", "some.branch"),
    VersionInfo(0, 1, 0, "dev2", "some.branch"),
    VersionInfo(0, 1, 0, "dev3", "some.other.branch"),
]


def test_versioning_asserts_prod_version_with_prod_version(
    mocker: MockerFixture,
) -> None:
    mocker.patch("builtins.open", mocker.mock_open(read_data=PYPROJECT_TOML_WITH_PROD_VERSION))

    with pytest.raises(SystemExit) as e:
        assert_prod_version()

    assert e.type == SystemExit
    assert e.value.code == 0


def test_versioning_asserts_prod_version_with_dev_version(
    mocker: MockerFixture,
) -> None:
    mocker.patch("builtins.open", mocker.mock_open(read_data=PYPROJECT_TOML_WITH_DEV_VERSION))

    with pytest.raises(SystemExit) as e:
        assert_prod_version()

    assert e.type == SystemExit
    assert e.value.code == 1


def test_assert_version_available_with_available_version(mocker: MockerFixture) -> None:
    mocker.patch("builtins.open", mocker.mock_open(read_data=PYPROJECT_TOML_WITH_PROD_VERSION))
    mocker.patch(
        "pylib.assert_version_available.get_package_versions",
        return_value=VERSIONS_AVAILABLE_WITH_VERSION_AVAILABLE,
    )

    with pytest.raises(SystemExit) as e:
        assert_version_available()

    assert e.type == SystemExit
    assert e.value.code == 0


def test_assert_version_available_with_not_available_version(
    mocker: MockerFixture, capsys: CaptureFixture[str]
) -> None:
    mocker.patch("builtins.open", mocker.mock_open(read_data=PYPROJECT_TOML_WITH_PROD_VERSION))
    mocker.patch(
        "pylib.assert_version_available.get_package_versions",
        return_value=VERSIONS_AVAILABLE_WITH_VERSION_NOT_AVAILABLE,
    )

    with pytest.raises(SystemExit) as e:
        assert_version_available()

    assert e.type == SystemExit
    assert e.value.code == 1
    assert (
        "Package rtb-apps-dev with version 0.1.0 already exists in repository. "
        "Did you forget to bump the version?\n" in capsys.readouterr().err
    )


def test_set_next_dev_version(mocker: MockerFixture) -> None:
    open_mock = mocker.patch("builtins.open", mocker.mock_open(read_data=PYPROJECT_TOML_WITH_PROD_VERSION))
    mocker.patch("pylib.set_next_dev_version.get_package_versions", return_value=DEV_VERSIONS)
    mocker.patch("pylib.set_next_dev_version.get_branch_tokenized", return_value="some.branch")
    mocker.patch("pylib.set_next_dev_version.is_on_main_branch", return_value=False)

    set_next_dev_version()
    args = (args[0] for name, args, _ in open_mock.mock_calls if name == "().write")
    assert b'version = "0.1.0-dev3+some.branch"\n' in args


@pytest.fixture(autouse=True)
def clear_lru_cache() -> None:
    get_pyproject.cache_clear()  # pylint: disable=protected-access
