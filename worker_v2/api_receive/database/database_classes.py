"""Module to handle database logic."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_recieve.database.models import TblStock, Template


class Database:
    """General Abstarct class."""

    def __init__(self, url: str, password: str) -> None:
        """General creation of database.

        Args:
            url: str - url to connect to
            password: str - password for database
        """
        self.engine = create_engine(url)
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
        return (
            self.session.
            query(TblStock).
            filter_by(lclientorderitemid=order_item).
            all()
        )


class PostgresDB(Database):
    """Postgresql Variant."""

    def get_template(self, template_id: str) -> Template | None:
        """Fetch template info.

        Args:
            template_id: str - template to fetch

        Returns:
            Template | None - template
        """
        return self.session.query(Template).filter_by(id=template_id).first()
