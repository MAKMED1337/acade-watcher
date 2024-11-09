from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class WatchedAccounts(Base):
    __tablename__ = 'watched_accounts'

    id: Mapped[str] = mapped_column(primary_key=True)
