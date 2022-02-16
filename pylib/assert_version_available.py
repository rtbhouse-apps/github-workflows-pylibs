import sys

from .common import get_current_version, get_package_name, get_package_versions
from .io import error


def assert_version_available() -> None:
    current_version = get_current_version()
    package_versions = get_package_versions(get_package_name())
    if str(current_version) in (str(package_version) for package_version in package_versions):
        error(
            f"Package {get_package_name()} with version {current_version} already exists in repository. Did you "
            "forget to bump the version?"
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    assert_version_available()
