from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

#Database was setup
engine = create_engine('sqlite:///canteen.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Category setup
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    items = relationship('MenuItem', backref='category', lazy=True)

#Menu item data stored
class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)

#Order data setup
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    student_name = Column(String, nullable=False)
    item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    item = relationship('MenuItem', backref='orders')

#Created the tables
Base.metadata.create_all(engine)
