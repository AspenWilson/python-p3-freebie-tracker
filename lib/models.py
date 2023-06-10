from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

company_dev = Table(
    'company_dev',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    devs = relationship('Dev', secondary=company_dev, back_populates='companies')
    freebies = relationship('Freebie', backref=backref('company'), cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Company: {self.name}>'

    @classmethod
    def get_freebies(cls, session):
        first_company = session.query(cls).first()
        return session.query(Freebie).filter(Freebie.company_id == first_company.id).all()

    @property
    def dev_names(self):
        return [dev.name for dev in self.devs]

    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        return new_freebie

    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    
    companies = relationship('Company', secondary=company_dev, back_populates='devs')
    freebies = relationship('Freebie', backref=backref('dev'), cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Dev: {self.name}>'

    @classmethod
    def get_freebies(cls, session):
        first_dev = session.query(cls).first()
        return session.query(Freebie).filter(Freebie.dev_id == first_dev.id).all()

    @property
    def company_names(self):
        return [company.name for company in self.companies]

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key =True)
    item_name= Column(String())
    value = Column(Integer())

    dev_id = Column(ForeignKey('devs.id'))
    company_id = Column(ForeignKey('companies.id'))


    def __repr__(self):
        return f'Freebie(id:{self.id}, ' + \
            f'Name:{self.item_name}, ' + \
            f'company_id:{self.company_id}, ' + \
            f'dev_id:{self.dev_id})'
    
    def print_details(self, session):
        dev_name = session.query(Dev.name).filter(Dev.id == self.dev_id).scalar()
        company_name = session.query(Company.name).filter(Company.id == self.company_id).scalar()
        return f'{dev_name} owns a {self.item_name} from {company_name}'


