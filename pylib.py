import argparse

from pylib import assert_prod_version, assert_version_available, set_next_dev_version


actions = {
    "assert-prod-version": assert_prod_version,
    "assert-version-available": assert_version_available,
    "set-next-dev-version": set_next_dev_version,
}


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "action",
    type=str,
    choices=actions.keys(),
)
args = parser.parse_args()
actions[args.action]()
