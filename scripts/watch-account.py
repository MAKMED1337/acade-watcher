import argparse

from watcher.db import session
from watcher.watched_accounts import WatchedAccounts

parser = argparse.ArgumentParser()
parser.add_argument('account_id')
args = parser.parse_args()


def main() -> None:
    with session() as db:
        db.add(WatchedAccounts(args.account_id))
        db.commit()


if __name__ == '__main__':
    main()
