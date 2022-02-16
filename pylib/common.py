from __future__ import annotations

import re
import subprocess
import sys
from functools import lru_cache
from typing import Any, Dict, List

import tomli
from pip._internal.commands import install
from pip._internal.network.session import PipSession

from .io import error
from .semver import VersionInfo


def get_package_versions(package_name: str) -> List[VersionInfo]:
    session = PipSession()
    x = install.InstallCommand("_", "_")
    options = x.parse_args([])[0]
    finder = x._build_package_finder(  # pylint: disable=protected-access
        options=options,
        session=session,
        target_python=None,
        ignore_requires_python=False,
    )
    candidates = finder.find_all_candidates(package_name)
    versions = [VersionInfo.parse(str(candidate.version)) for candidate in candidates]
    return versions


@lru_cache
def get_branch() -> str:
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, check=False)
    if result.returncode != 0:
        error(result.stderr.decode("utf-8"))
        sys.exit(1)
    return result.stdout.decode("utf-8").strip()


def get_branch_tokenized() -> str:
    return re.sub(
        r"\.+",
        ".",
        get_branch().lower().replace("-", ".").replace("_", ".").replace("/", "."),
    )


def is_on_main_branch() -> bool:
    return get_branch() in ("main", "master")


@lru_cache
def get_pyproject() -> Dict[str, Any]:
    with open("pyproject.toml", "rb") as f:
        return tomli.load(f)


def get_package_name() -> str:
    name = get_pyproject()["tool"]["poetry"]["name"]
    assert isinstance(name, str)
    return name


def get_current_version() -> VersionInfo:
    return VersionInfo.parse(get_pyproject()["tool"]["poetry"]["version"])


def get_current_version_finalized() -> VersionInfo:
    return get_current_version().finalize_version()
