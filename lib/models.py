from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean,create_engine
from sqlalchemy.orm import relationship, backref,declarative_base
# from sqlalchemy.ext.declarative import declarative_base

# convention = {
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# }
# metadata = MetaData(naming_convention=convention)

Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    phone = Column(String())

    role = relationship('Role', backref=backref('roles.id', useList='false'))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    auditions = relationship("Audition", back_populates="role")

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if hired_auditions:
            return hired_auditions[0]
        return 'No actor has been hired for this role.'

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        return 'No actor has been hired for understudy for this role.'
    
class Audition(Base):
    __tablename__ = 'actors'
    id = Column(Integer(), primary_key=True)
    actor = Column(Integer())
    location = Column(String())
    phone = Column(String())
    hired = Column(Boolean)

    role_id = Column(Integer(),ForeignKey('roles.id'))

    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = True
        
if __name__ == "__main__":
    engine = create_engine("sqlite:///theater.db")
    Base.metadata.create_all(engine)        