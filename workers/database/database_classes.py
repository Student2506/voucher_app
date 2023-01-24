"""Module to handle database logic."""

from urllib.parse import quote_plus
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from workers.database.models import TblStock, Template


class Database:
    """General Abstarct class."""

    def __init__(self, url: str, password: str) -> None:
        """General creation of database.

        Args:
            url: str - url to connect to
            password: str - password for database
        """
        self.engine = create_engine(url % quote_plus(password))
        self.session = Session(self.engine)


class MSSQLDB(Database):
    """MSSQL Variant."""

    def get_table_stock(self, order_item: str) -> list[TblStock]:
        """Fetch stock item.

        Args:
            order_item: str - order item to take

        Returns:
            list[TblStock] - order items
        """
        return list(self.session.query(TblStock).filter_by(lclientorderitemid=order_item))


class PostgresDB(Database):
    """Postgresql Variant."""

    def get_template(self, template_id: UUID) -> Template | None:
        """Fetch template info.

        Args:
            template_id: UUID - template to fetch

        Returns:
            Template | None - template
        """
        return self.session.query(Template).filter_by(id=template_id).first()
