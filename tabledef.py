from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, TIMESTAMP, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

#engine = create_engine('sqlite:///listings.db', echo=True)
db_host = 'postgreinstance1.cmqiuzqh62x2.us-east-1.rds.amazonaws.com'
db_port = 5432
db_name = "dbpostgre1"
db_user = "postgremaster1"
db_pass = "postgremaster1"

engine = create_engine('postgresql://'+db_user+':'+db_pass+'@'+db_host+':'+str(db_port)+'/'+db_name, echo=True)
Base = declarative_base()


########################################################################
class Listing(Base):
    """"""
    __tablename__ = "listing"

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    category_id = Column(String)
    item_id = Column(String)
    seller = Column(String)
    price = Column(DECIMAL)
    available_quantity = Column(INTEGER)
    sold_quantity = Column(INTEGER)
    UF = Column(String)
    free_shipping = Column(BOOLEAN)
    title = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, timestamp, category_id, item_id, seller, price, available_quantity, sold_quantity, UF, free_shipping, title):
        """"""
        self.timestamp = timestamp
        self.category_id = category_id
        self.item_id = item_id
        self.seller = seller
        self.price = price
        self.available_quantity = available_quantity
        self.sold_quantity = sold_quantity
        self.UF = UF
        self.free_shipping = free_shipping
        self.title = title


# create tables
Base.metadata.create_all(engine)