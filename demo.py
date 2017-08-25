import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///listings.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Create objects
for anuncio in session.query(Listing).order_by(Listing.id):
    print (anuncio.item_id, anuncio.price)