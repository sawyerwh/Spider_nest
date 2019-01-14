from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/maoyan_db?charset=utf8", max_overflow=5,encoding='utf-8') 
Base = declarative_base()

class MogujieProduct(Base):
    __tablename__ = 'mogujie_product'
    id = Column(Integer, primary_key=True, autoincrement=True)    #主键，自增
    tradeitemid = Column(String(512))
    itemtype = Column(String(512))
    img = Column(String(1024))
    clienturl = Column(String(1024))
    link = Column(String(1024))
    itemmarks = Column(String(512))
    acm = Column(String(512))
    title = Column(String(512))
    cparam = Column(String(512))
    orgprice = Column(String(512))
    hassimilarity = Column(String(512))
    sale = Column(String(512))
    cfav = Column(String(512))
    price = Column(String(512))
    similarityurl = Column(String(1024))
