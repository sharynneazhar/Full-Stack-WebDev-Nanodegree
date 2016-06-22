from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)

class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(8), nullable=False)
    picture = Column(String)
    dateOfBirth = Column(Date)
    weight = Column(Numeric(10))
    shelter = relationship(Shelter)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
