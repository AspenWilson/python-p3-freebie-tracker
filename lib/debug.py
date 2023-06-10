#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    first_freebie = session.query(Freebie).first()
    Freebie.dev = session.query(Dev).filter(Dev.id == first_freebie.dev_id).all()
    Freebie.company = session.query(Company).filter(Company.id == first_freebie.company_id).all()

    first_company = session.query(Company).first()
    Company.freebies = Company.get_freebies(session)
    Company.devs = [session.query(Dev).get(Freebie.dev_id) for Freebie in Company.freebies]

    first_dev = session.query(Dev).first()
    Dev.freebies = Dev.get_freebies(session)
    Dev.companies = [session.query(Company).get(Freebie.company_id) for Freebie in Dev.freebies]

    import ipdb; ipdb.set_trace()