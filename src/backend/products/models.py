from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Identity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class ProductData(Base):
    __tablename__ = 'ProductData'

    id = Column(Integer, Identity(), primary_key=True)
    product_id = Column(String(255), nullable=False)
    attribute_name = Column(String(255), nullable=False)
    attribute_value = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<ProductData(id={self.id}, product_id='{self.product_id}', attribute_name='{self.attribute_name}', attribute_value='{self.attribute_value}')>"

class Products(Base):
    __tablename__ = 'Products'

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Products(id={self.id}, name='{self.name}')>"

class ProductAttributes(Base):
    __tablename__ = 'ProductAttributes'

    id = Column(Integer, Identity(), primary_key=True)
    product_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<ProductAttributes(id={self.id}, product_id={self.product_id}, name='{self.name}', value='{self.value}')>"

class ProductMatching(Base):
    __tablename__ = 'ProductMatching'

    id = Column(Integer, Identity(), primary_key=True)
    product_id1 = Column(Integer, nullable=False)
    product_id2 = Column(Integer, nullable=False)
    similarity_score = Column(Float, nullable=False)
    matched_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<ProductMatching(id={self.id}, product_id1={self.product_id1}, product_id2={self.product_id2}, similarity_score={self.similarity_score})>"

def create_database(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session