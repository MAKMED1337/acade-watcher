from sqlalchemy import JSON, BigInteger, func, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from .db import Base


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
