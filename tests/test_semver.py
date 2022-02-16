from typing import Mapping

import pytest

from pylib.semver import VersionInfo


@pytest.mark.parametrize(
    "version_str,expected_version_info",
    [
        ("1.2.3", VersionInfo(major=1, minor=2, patch=3)),
        ("1.2.3-dev0", VersionInfo(major=1, minor=2, patch=3, prerelease="dev0")),
        ("1.2.3-alpha1", VersionInfo(major=1, minor=2, patch=3, prerelease="alpha1")),
        ("1.2.3.dev0", VersionInfo(major=1, minor=2, patch=3, prerelease="dev0")),
        ("0.0.1.dev3", VersionInfo(major=0, minor=0, patch=1, prerelease="dev3")),
        (
            "0.0.1.dev3+build.info",
            VersionInfo(major=0, minor=0, patch=1, prerelease="dev3", build="build.info"),
        ),
        (
            "0.0.1-dev3+build.info",
            VersionInfo(major=0, minor=0, patch=1, prerelease="dev3", build="build.info"),
        ),
    ],
)
def test_version_info_parses_semver(version_str: str, expected_version_info: VersionInfo) -> None:
    assert VersionInfo.parse(version_str) == expected_version_info


@pytest.mark.parametrize(
    "version_str",
    [
        "1",
        "1.2",
        "1-2-3",
        "1.2.3dev",
        "1.2.3_dev4",
        "1.2.3+test_build",
        "1.2.3-dev0+test_build",
    ],
)
def test_version_info_fails_to_parse_invalid_semver(version_str: str) -> None:
    with pytest.raises(ValueError):
        VersionInfo.parse(version_str)


@pytest.mark.parametrize(
    "version_info,parts,expected_version_info",
    [
        (
            VersionInfo(major=1, minor=2, patch=3),
            {"major": 2},
            VersionInfo(major=2, minor=2, patch=3),
        ),
        (
            VersionInfo(major=1, minor=2, patch=3),
            {"minor": 3, "patch": 5},
            VersionInfo(major=1, minor=3, patch=5),
        ),
        (
            VersionInfo(major=1, minor=2, patch=3, prerelease="dev0"),
            {"prerelease": "dev1"},
            VersionInfo(major=1, minor=2, patch=3, prerelease="dev1"),
        ),
        (
            VersionInfo(major=1, minor=2, patch=3, prerelease="dev0"),
            {"build": "test.build"},
            VersionInfo(major=1, minor=2, patch=3, prerelease="dev0", build="test.build"),
        ),
    ],
)
def test_version_info_replaces_parts(
    version_info: VersionInfo,
    parts: Mapping[str, str | int],
    expected_version_info: VersionInfo,
) -> None:
    assert version_info.replace(**parts) == expected_version_info


def test_version_info_compares_versions() -> None:
    assert max(
        [
            VersionInfo.parse("1.2.3"),
            VersionInfo.parse("1.2.4"),
            VersionInfo.parse("1.2.5.dev2"),
            VersionInfo.parse("1.2.5.dev0"),
            VersionInfo.parse("1.2.5.dev3"),
        ]
    ) == VersionInfo.parse("1.2.5.dev3")


@pytest.mark.parametrize(
    "version_str,token,expected_version_info",
    [
        (
            "1.2.3.dev2",
            "dev",
            VersionInfo(major=1, minor=2, patch=3, prerelease="dev3"),
        ),
        ("1.2.3", "dev", VersionInfo(major=1, minor=2, patch=3, prerelease="dev.1")),
        (
            "1.2.3-alpha0",
            "alpha",
            VersionInfo(major=1, minor=2, patch=3, prerelease="alpha1"),
        ),
        (
            "1.2.3-beta3",
            "beta",
            VersionInfo(major=1, minor=2, patch=3, prerelease="beta4"),
        ),
    ],
)
def test_version_info_bumps_prerelease(version_str: str, token: str, expected_version_info: VersionInfo) -> None:
    assert VersionInfo.parse(version_str).bump_prerelease(token=token) == expected_version_info


def test_dev_version_with_two_numbers_is_higher_then_with_one_number() -> None:
    assert VersionInfo.parse("1.2.5-dev10") > VersionInfo.parse("1.2.5-dev9")
