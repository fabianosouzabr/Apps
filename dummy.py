import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///listings.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Create objects
anuncio = Listing(datetime.datetime.now(), "category_id1", "item_id1", "seller1", 1.01, 10, 100, "BR-SP",True , "title 1 Foo")
session.add(anuncio)

anuncio = Listing(datetime.datetime.now(), "category_id2", "item_id2", "seller2",221.02, 20, 2100, "BR-rj",False , "title 2 Bar")
session.add(anuncio)

anuncio = Listing(datetime.datetime.now(), "category_id3", "item_id3", "seller3", 3331.01 , 31, 31300, "BR-MG",True , "title 3 Baz")
session.add(anuncio)

# commit the record the database
session.commit()