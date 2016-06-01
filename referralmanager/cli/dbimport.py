import importlib
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
@click.option('--referral-type', type=click.Choice(['AlasccaBloodReferral', 'AlasccaTissueReferral']), required=True)
@click.pass_context
def dbimport(ctx, dbcred, local_data_dir, referral_type):
    logging.info("Running database import from dir {}".format(local_data_dir))
    cred_conf = json.load(dbcred)

    engine = create_tables(cred_conf['dburi'])
    session = get_session(engine)

    module = importlib.import_module('referralmanager.cli.models.referrals')
    referral_class = getattr(module, referral_type)

    import_referrals(session, local_data_dir, referral_class)


def create_tables(uri):
    engine = create_engine(uri, echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def import_referrals(session, searchdir, referral_class, fileending="csv"):
    files = [f for f in os.listdir(searchdir) if f.endswith(fileending)]
    for fn in files:
        with open(os.path.join(searchdir, fn), 'r') as f:
            header = f.readline()
            for ln in f:
                ref = referral_class(ln)
                session.add(ref)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
