#!/usr/bin/env python3
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

fake = Faker()

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()

    fake = Faker()

    companies = []
    for i in range(50):
        company = Company(
            name = fake.name(),
            founding_year = random.randint(1965,2023)
        )

        # add and commit individually to get IDs back
        session.add(company)
        session.commit()

        companies.append(company)
    
    devs = []
    for i in range(25):
        dev = Dev(
            name=fake.name(),
        )

        session.add(dev)
        session.commit()

        devs.append(dev)

    freebies = []
    for company in companies:
        for i in range(random.randint(1,5)):
            dev = random.choice(devs)
            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()
            
            freebie = Freebie(
                item_name=fake.name(),
                value=random.randint(0, 50),
                company_id=company.id,
                dev_id=dev.id,
            )

            freebies.append(freebie)

    session.bulk_save_objects(freebies)
    session.commit()
    session.close()

# def delete_records():
#     session.query(Company).delete()
#     session.query(Dev).delete()
#     session.query(Freebie).delete()
#     session.commit()

# def create_records():
#     companies = [Company() for i in range(100)]
#     devs = [Dev() for i in range(1000)]
#     freebies = [Freebie() for i in range(500)]
#     session.add_all(companies + devs + freebies)
#     session.commit()
#     return companies, devs, freebies

# def relate_records(companies, devs, freebies):
#     for freebie in freebies:
#         freebie.company = rc(companies)
#         freebie.dev = rc(devs)

#     session.add_all(freebies)
#     session.commit()

# if __name__ == '__main__':
#     delete_records()
#     companies, devs, freebies = create_records()
#     relate_records(companies, devs, freebies)