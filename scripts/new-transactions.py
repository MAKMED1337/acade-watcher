from watcher.db import session
from watcher.transactions import Transactions


def main() -> None:
    with session() as db:
        for tx in Transactions.get_unprocessed_transactions(db):
            print(tx.account_id, tx.tx_hash, tx.mnear)


if __name__ == '__main__':
    main()

