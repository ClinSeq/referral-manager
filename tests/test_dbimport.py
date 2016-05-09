import os
import unittest

from referralmanager.cli.dbimport import create_tables, import_blood_referrals, get_session, import_tissue_referrals
from referralmanager.cli.models.referrals import AlasccaBloodReferral, AlasccaTissueReferral


class TestDbImport(unittest.TestCase):
    def test_import_bloodreferral(self):
        engine = create_tables('sqlite:///:memory:')
        session = get_session(engine)

        blood_searchdir = os.path.join('tests', AlasccaBloodReferral.type_string)
        import_blood_referrals(session, blood_searchdir)

        assert len(session.query(AlasccaBloodReferral).all()) == 1

        # Try to import the same referral again, should do nothing
        import_blood_referrals(session, blood_searchdir)
        assert len(session.query(AlasccaBloodReferral).all()) == 1

    def test_import_tissuereferral(self):
        engine = create_tables('sqlite:///:memory:')
        session = get_session(engine)

        tissue_searchdir = os.path.join('tests', AlasccaTissueReferral.type_string)
        import_tissue_referrals(session, tissue_searchdir)

        assert len(session.query(AlasccaTissueReferral).all()) == 2

        # Try to import the same referral again, should do nothing
        import_tissue_referrals(session, tissue_searchdir)
        assert len(session.query(AlasccaTissueReferral).all()) == 2
