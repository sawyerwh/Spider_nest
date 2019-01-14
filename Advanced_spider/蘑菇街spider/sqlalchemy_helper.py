from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from mogujie_models import MogujieProduct

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1/maoyan_db?charset=utf8", max_overflow=5)
session_maker = sessionmaker(bind=engine)
session = session_maker()

def save_db(result_list):
    for item_dict in result_list:
        mogu = MogujieProduct()
     
        mogu.tradeitemid = item_dict['tradeItemId']
        mogu.itemtype = item_dict['itemType']
        mogu.img = item_dict['img']
        mogu.clienturl = item_dict['clientUrl']
        mogu.link = item_dict['link']
        mogu.itemmarks = item_dict['itemMarks']
        mogu.acm = item_dict['acm']
        mogu.title = item_dict['title']
        mogu.cparam = item_dict['cparam']
        mogu.orgprice = item_dict['orgPrice']
        mogu.hassimilarity = item_dict['hasSimilarity']
        mogu.sale = item_dict['sale']
        mogu.cfav = item_dict['cfav']
        mogu.price = item_dict['price']
        mogu.similarityurl = item_dict['similarityUrl']

        session.add(mogu)
        session.commit()    



