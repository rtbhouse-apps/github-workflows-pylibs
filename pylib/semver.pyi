# TODO: remove this stub after "semver" is updated to 3.x
# https://python-semver.readthedocs.io/en/latest/changelog.html

from typing import Optional, Tuple

class VersionInfo:
    build: str
    prerelease: str
    def __init__(
        self,
        major: int,
        minor: int = 0,
        patch: int = 0,
        prerelease: Optional[str | int] = None,
        build: Optional[str | int] = None,
    ): ...
    @classmethod
    def parse(cls, version: str) -> VersionInfo: ...
    def bump_prerelease(self, token: str) -> VersionInfo: ...
    def finalize_version(self) -> VersionInfo: ...
    def replace(self, **parts: str | int) -> VersionInfo: ...
    def to_tuple(self) -> Tuple[int, int, int, Optional[str | int], Optional[str | int]]: ...
    def __lt__(self, other: VersionInfo) -> bool: ...

def cmp(a: int, b: int) -> int: ...
def _nat_cmp(a: str, b: str) -> int: ...
