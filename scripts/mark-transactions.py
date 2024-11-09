import argparse

from watcher.db import session
from watcher.transactions import Transactions

parser = argparse.ArgumentParser()
parser.add_argument('account_id')
parser.add_argument('message')
args = parser.parse_args()


def main() -> None:
    with session() as db:
        Transactions.mark_new_transactions(db, args.account_id, args.message)
        db.commit()


if __name__ == '__main__':
    main()
