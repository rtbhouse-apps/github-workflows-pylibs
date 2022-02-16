from __future__ import annotations

import re
from typing import List

import semver

_prerelease_regex = re.compile(r"^([a-zA-Z]+)\.?(\d*)")


class VersionInfo(semver.VersionInfo):
    _REGEX = re.compile(
        r"""
        ^
        (?P<major>0|[1-9]\d*)
        \.
        (?P<minor>0|[1-9]\d*)
        \.
        (?P<patch>0|[1-9]\d*)
        (?:(?:-|\.)(?P<prerelease>
            (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
            (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
        ))?
        (?:\+(?P<build>
            [0-9a-zA-Z-]+
            (?:\.[0-9a-zA-Z-]+)*
        ))?
        $
    """,
        re.VERBOSE,
    )

    def replace(self, **parts: str | int) -> VersionInfo:
        return VersionInfo(*super().replace(**parts).to_tuple())


def _net_cmp(a: str, b: str) -> int:
    def convert(text) -> str | int:
        return int(text) if re.match("^[0-9]+$", text) else text

    def split_key(key) -> List[str | int]:
        match = _prerelease_regex.match(key)
        if match:
            groups = match.groups()
        else:
            groups = key.split(".")
        return [convert(c) for c in groups]

    def cmp_prerelease_tag(a, b) -> int:
        if isinstance(a, int) and isinstance(b, int):
            return semver.cmp(a, b)
        elif isinstance(a, int):
            return -1
        elif isinstance(b, int):
            return 1
        else:
            return semver.cmp(a, b)

    a, b = a or "", b or ""
    a_parts, b_parts = split_key(a), split_key(b)
    for sub_a, sub_b in zip(a_parts, b_parts):
        cmp_result = cmp_prerelease_tag(sub_a, sub_b)
        if cmp_result != 0:
            return cmp_result

    return semver.cmp(len(a), len(b))


semver._nat_cmp = _net_cmp  # pylint: disable=protected-access
