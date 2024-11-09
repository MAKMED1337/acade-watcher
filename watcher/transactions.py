from sqlalchemy import JSON, BigInteger, func, insert, literal, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from watcher.watched_accounts import WatchedAccounts

from .db import Base
from .processed_transactions import ProcessedTransactions


class Transactions(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_id: Mapped[str]

    # Withdrawal info
    status: Mapped[bool]
    args: Mapped[dict] = mapped_column(JSON)  # in general
    mnear: Mapped[int]

    # Tx info
    tx_hash: Mapped[str]
    block_hash: Mapped[str]
    receipt_id: Mapped[str]

    comment: Mapped[str | None]

    @staticmethod
    def get_last_id(db: Session) -> int | None:
        return db.execute(select(func.max(Transactions.id))).scalar_one_or_none()

    @staticmethod
    def get_watched_transactions(db: Session) -> list[tuple['Transactions', ProcessedTransactions | None]]:
        return (
            db.query(Transactions, ProcessedTransactions)
            .outerjoin(ProcessedTransactions)
            .where(Transactions.account_id.in_(select(WatchedAccounts.id)))
            .all()
        )  # type: ignore[return-value]

    @staticmethod
    def get_unprocessed_transactions(db: Session) -> list['Transactions']:
        return (
            db.query(Transactions)
            .outerjoin(ProcessedTransactions)
            .where(Transactions.account_id.in_(select(WatchedAccounts.id)), ProcessedTransactions.id == None)  # noqa: E711
            .all()
        )

    @staticmethod
    def mark_new_transactions(db: Session, account_id: str, message: str) -> None:
        db.execute(
            insert(ProcessedTransactions).from_select(
                ['id', 'status'],
                select(Transactions.id, literal(message)).where(
                    Transactions.account_id == account_id, Transactions.id.not_in(select(ProcessedTransactions.id))
                ),
            )
        )
