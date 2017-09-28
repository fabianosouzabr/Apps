# coding: utf-8
#! /usr/bin/python3

import os
import sys
import datetime
from sqlalchemy.orm import sessionmaker
from tabledef import *

db_host = 'postgreinstance1.cmqiuzqh62x2.us-east-1.rds.amazonaws.com'
db_port = 5432
db_name = "dbpostgre1"
db_user = "postgremaster1"
db_pass = "postgremaster1"
engine = create_engine('postgresql://'+db_user+':'+db_pass+'@'+db_host+':'+str(db_port)+'/'+db_name, echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

LIB_PATH = os.path.join('.', 'python3-sdk', 'lib')
print(LIB_PATH)
sys.path.append(LIB_PATH)
from meli import Meli

CLIENT_ID = '6383285056445610'
CLIENT_SECRET = 'Zya79p7R8hLkQaRfficgmEA8bNf30a7B'
REDIRECT_URI = '''http://localhost:4567/redirect'''
CLIENT_NAME = 'Stranger'

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

category_list = ['MLB223835']

for category in category_list:
    paging_limit = 200
    paging_offset = 0
    items_total = 0
    foo = 1
    timestamp = datetime.datetime.now()
    while paging_offset <= items_total:
        response = (meli.get("/sites/MLB/search?category=" + category + "&condition=new&buying_mode=buy_it_now" + "&offset=" + str(paging_offset) + "&limit=" + str(paging_limit)+"&sort=relevance"))
        jresponse = response.json()
        #timestamp = response.headers['date']
        paging_limit = jresponse['paging']['limit']
        items_total = jresponse['paging']['total']
        item_results  = jresponse['results']
        for item in item_results:
            category_id = item['category_id']
            item_id=item['id']
            seller=item['seller']['id']
            price=item['price']
            available_quantity=item['available_quantity']
            sold_quantity=item['sold_quantity']
            UF=item['address']['state_id']
            free_shipping=item['shipping']['free_shipping']
            title=item['title']
            # Create objects
            anuncio = Listing(timestamp, category_id, item_id, seller, price, available_quantity, sold_quantity, UF, free_shipping, title)
            session.add(anuncio)
            #print(timestamp, foo, "/" , items_total, category_id , paging_offset, item_id, seller,UF, free_shipping, price, available_quantity, sold_quantity, title )
            #foo += 1
        paging_offset += paging_limit

# commit the record the database
session.commit()