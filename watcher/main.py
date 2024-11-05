import json
import logging
import time
from typing import Any

import requests
from sqlalchemy.orm import Session

from .config import settings
from .db import session
from .db import start as start_db
from .transactions import Transactions


def parse_transaction(tx: dict[str, Any]) -> Transactions:
    action = tx['actions'][0]
    args = json.loads(action['args'])
    return Transactions(
        id=int(tx['id']),
        account_id=tx['predecessor_account_id'],
        status=tx['outcomes']['status'],
        args=args,
        mnear=args['mnear'],
        tx_hash=tx['transaction_hash'],
        block_hash=tx['receipt_block']['block_hash'],
        receipt_id=tx['receipt_id'],
        comment=None if len(tx['actions']) == 1 else 'FIXME: more than 1 action',
    )


# Returns the maximum id if there are more data (because queries are using strictly greater) or none otherwise
def process_new_blocks(db: Session) -> int | None:
    cursor = Transactions.get_last_id(db)
    headers = {
        'Authorization': f'Bearer {settings.API_KEY}',
    }

    params = {
        'method': 'withdraw',
        'cursor': cursor,
        'order': 'asc',
    }

    j = {'message': 'No message ???'}
    try:
        resp = requests.get(
            'https://api.nearblocks.io/v1/account/studio.acade.near/txns', params=params, headers=headers, timeout=10
        )
        j = resp.json()
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        logging.error('API timeout')  # noqa: TRY400
        return False
    except requests.exceptions.HTTPError:
        logging.exception('API error: %s', j['message'])
        return False

    db.add_all([parse_transaction(tx) for tx in j['txns']])
    if 'cursor' in j:
        return int(j['cursor'])
    return None


def main() -> None:
    start_db()
    while True:
        for retry in range(settings.MAX_RETRIES):
            with session() as db, db.begin():
                next_id = process_new_blocks(db)
            if next_id is None:
                break
            logging.info('Retrying(%d) from %d', retry + 1, next_id)

        time.sleep(settings.DELAY)


if __name__ == '__main__':
    main()
