import sys

from .common import get_current_version
from .io import error


def assert_prod_version() -> None:
    if get_current_version().prerelease is not None:
        error(f"Version {get_current_version()} isn't final. Please provide final version in pyproject.toml.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    assert_prod_version()
