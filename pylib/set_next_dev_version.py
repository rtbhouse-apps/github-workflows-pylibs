import sys
from copy import deepcopy

import tomli_w

from .common import (
    get_branch_tokenized,
    get_current_version_finalized,
    get_package_name,
    get_package_versions,
    get_pyproject,
    is_on_main_branch,
)
from .io import error
from .semver import VersionInfo


def _get_next_dev_version() -> VersionInfo:
    all_versions = get_package_versions(get_package_name())
    current_dev_versions = [
        version
        for version in all_versions
        if version.finalize_version() == get_current_version_finalized() and version.build == get_branch_tokenized()
    ]
    if current_dev_versions:
        next_dev_version = max(current_dev_versions).bump_prerelease(token="dev")
    else:
        next_dev_version = get_current_version_finalized().replace(prerelease="dev0")
    return next_dev_version.replace(build=get_branch_tokenized())


def set_next_dev_version() -> None:
    if is_on_main_branch():
        error("This operation can only be performed on development branch")
        sys.exit(1)

    pyproject = deepcopy(get_pyproject())
    next_dev_version = _get_next_dev_version()
    with open("pyproject.toml", "wb") as f:
        pyproject["tool"]["poetry"]["version"] = str(next_dev_version)
        tomli_w.dump(pyproject, f)


if __name__ == "__main__":
    set_next_dev_version()
