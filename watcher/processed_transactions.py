from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class ProcessedTransactions(Base):
    __tablename__ = 'processed_transactions'

    id: Mapped[int] = mapped_column(ForeignKey('transactions.id'), primary_key=True)
    status: Mapped[str]
