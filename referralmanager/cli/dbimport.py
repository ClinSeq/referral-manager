import json
import logging
import os

import click
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from referralmanager.cli.models.referrals import Base, AlasccaBloodReferral, AlasccaTissueReferral


@click.command()
@click.option('--dbcred', type=click.File('r'), required=True)
@click.option('--local-data-dir', type=str, required=True)
@click.pass_context
def dbimport(ctx, dbcred, local_data_dir):
    logging.info("Running database import from dir {}".format(local_data_dir))
    cred_conf = json.load(dbcred)

    engine = create_tables(cred_conf['dburi'])
    session = get_session(engine)

    blood_searchdir = os.path.join(local_data_dir, AlasccaBloodReferral.type_string)
    import_blood_referrals(session, blood_searchdir)

    tissue_searchdir = os.path.join(local_data_dir, AlasccaTissueReferral.type_string)
    import_tissue_referrals(session, tissue_searchdir)


def create_tables(uri):
    engine = create_engine(uri, echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def import_blood_referrals(session, searchdir, fileending="csv"):
    files = [f for f in os.listdir(searchdir) if f.endswith(fileending)]
    for fn in files:
        with open(os.path.join(searchdir, fn), 'r') as f:
            header = f.readline()
            for ln in f:
                ref = AlasccaBloodReferral(ln)
                session.add(ref)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()


def import_tissue_referrals(session, searchdir, fileending="csv"):
    files = [f for f in os.listdir(searchdir) if f.endswith(fileending)]
    for fn in files:
        with open(os.path.join(searchdir, fn), 'r') as f:
            header = f.readline()
            for ln in f:
                ref = AlasccaTissueReferral(ln)
                session.add(ref)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
