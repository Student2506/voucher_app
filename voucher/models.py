from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class ContrAgent:

    def __init__(self, host, database, user, password):

        self.connection_url = URL.create(
            'mssql+pyodbc',
            username=user,
            password=password,
            host=host,
            port=1433,
            database=database,
            query={
                # 'driver': 'ODBC Driver 17 for SQL Server',
                'driver': 'SQL Server',
                'authentication': 'SqlPassword',
                'TrustServerCertificate': 'Yes',
            },
        )
        self.engine = create_engine(self.connection_url, future=True)
        self.metadata = MetaData()
        self.metadata.reflect(self.engine, only=[
            'tblClient',
            'tblClientOrder',
            'tblClientOrderItem',
            'tblVoucherType',
            'tblStock',
        ])
        Base = automap_base(metadata=self.metadata)
        Base.prepare()
        self.client = Base.classes.tblClient
        self.client_order = Base.classes.tblClientOrder
        self.client_order_item = Base.classes.tblClientOrderItem
        self.voucher_type = Base.classes.tblVoucherType
        self.stock = Base.classes.tblStock
        self.session = Session(self.engine)
