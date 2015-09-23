from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Numeric,
    Float,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class City(Base):
    """US City model"""
    __tablename__ = 'us_cities'
    zip = Column(Integer, primary_key=True)
    state = Column(Text, primary_key=True)
    city = Column(Text)
    lat = Column(Float)
    lng = Column(Float)

    def __init__(self, zip, state, city, lat, lng):
        self.zip = zip
        self.state = state
        self.city = city
        self.lat = lat
        self.lng = lng

    @classmethod
    def get_city(cls, code):
        """Get city from zip code"""
        city = DBSession.query(City).filter_by(zip=code).first()
        if city is None:
            return None
        return city.get_json()

    def get_json(self):
        """Get json object for city"""
        return dict(
            zip=self.zip, state=self.state, city=self.city,
            lat=float(self.lat), lng=float(self.lng)
        )
