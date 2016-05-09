# `referral-manager`

[![Build Status](https://travis-ci.org/ClinSeq/referral-manager.svg?branch=master)](https://travis-ci.org/ClinSeq/referral-manager) [![Code Health](https://landscape.io/github/ClinSeq/referral-manager/master/landscape.svg?style=flat)](https://landscape.io/github/ClinSeq/referral-manager/master)

`referral-manager` is a packages to download new referrals from the KI Biobank customer FTP and add them to the local mysql referral database. 

## Command line 

`refman` is the main command for the package. It has two subcomponents, `fetch` and `dbimport`. 

### `fetch`

TBD. 

Downloads CSV files and PDF with new referrals from KI Biobank customer FTP. 

### `dbimport`

`refman dbimport --dbcred config.json --local-data-dir /nfs/ALASCCA/referrals` finds CSV files in the subdirectories `ALASCCA_blod` and `ALASCCA_colon_rektum` into the tables `bloodreferals` and `tissuereferrals`, respectively. `config.json` should be a json file like so: 

~~~json
{
  "dburi": "sqlite:///:memory:" // replace with proper sqlalchemy connection string
}
~~~

## API

Developers can use the classes `AlasccaBloodReferral` and `AlasccaTissueReferral` to handle referral data in other packages. 
