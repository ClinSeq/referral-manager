import json
import logging
import os
import pysftp
import sys

import click


def get_login_details(login_file):
    try:
        login_details = json.load(open(login_file))
        username = login_details["username"]
        password = login_details["password"]
    except Exception, e:
        logging.error("Failed to process login file: " + e)
        raise
    return (username, password)


def recursive_list(sftp_conn, dir):
  curr_list = []
  def appendToList(item):
    curr_list.append(item)
  sftp_conn.walktree(dir, appendToList, appendToList, appendToList)
  return curr_list


def match_extn(path, extn):
  elems = path.split(".")
  if len(elems) > 0 and elems[-1] == extn:
    return True
  else:
    return False


def setup_local_dir(local_data_dir):
    '''Check that the specified data directory exists, and generate csv
    and pdf directories within it if they do not already exist.'''

    if not os.path.exists(local_data_dir):
        logging.error("Error: Specified local data directory does not exist: " +
                      local_data_dir)
        sys.exit(1)

    # Make local csv and pdf directories if they do not exist:
    csv_dir = os.path.join(local_data_dir, "csv")
    pdf_dir = os.path.join(local_data_dir, "pdf")
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)
    if not os.path.exists(pdf_dir):
        os.mkdir(pdf_dir)

    return (csv_dir, pdf_dir)


def download_files(conn, remote_files, local_dir):
    '''Download the specified remote files to the specified local directory
    using the given sftp connection.'''

    logging.info("Downloading {} files to {}".format(len(remote_files), local_dir))

    for curr_file in remote_files:
        remote_file_name = os.path.split(curr_file)[1]
        try:
            logging.info("{}".format(curr_file))
            conn.get(curr_file, localpath=os.path.join(local_dir, remote_file_name))
        except Exception:
            logging.error("ERROR: File failed to download: {}".format(curr_file))
            raise


@click.command()
@click.option('--login_file', type=str, default=os.path.expanduser("~/.refslogin"))
@click.option('--local-data-dir', type=str, required=True,
              default='')
@click.option('--remote-data-dir', type=str, required=True)
@click.pass_context
def fetch(ctx, login_file, local_data_dir, remote_data_dir):
    '''Copy new referrals from the specified folder on the remote sftp server to the local data directory.

    Recursively identify all csv and pdf files in the remote data folder and if any are new then copy them
    to respective csv and pdf folders within the local data folder. Generates the csv and pdf folders if
    they do not already exist.
'''

    logging.info("Running fetch: Fetching from {} to {}".format(remote_data_dir, local_data_dir))

    (username, password) = get_login_details(login_file)

    # Identify all relevant remote files:
    conn = pysftp.Connection('kundftp.biobank.ki.se', username=username, password=password)
    remote_listing = recursive_list(conn, remote_data_dir)
    remote_csv = filter(lambda curr_path: match_extn(curr_path, "csv"), remote_listing)
    remote_pdf = filter(lambda curr_path: match_extn(curr_path, "pdf"), remote_listing)

    # Check and setup specified local directory:
    (csv_dir, pdf_dir) = setup_local_dir(local_data_dir)

    # Identify all relevant local files:
    local_csv = set([filename for dir_path, dir_name, filenames in
                     os.walk(csv_dir) for filename in filenames])
    local_pdf = set([filename for dir_path, dir_name, filenames in
                     os.walk(pdf_dir) for filename in filenames])

    # Obtain a list of csv and pdf files present remotely but not locally:
    csv_to_download = filter(lambda remote_file: not(os.path.split(remote_file)[1] in local_csv), remote_csv)
    pdf_to_download = filter(lambda remote_file: not(os.path.split(remote_file)[1] in local_pdf), remote_pdf)

    # Download the resulting files to the respective local csv and pdf folders:
    download_files(conn, csv_to_download, csv_dir)
    download_files(conn, pdf_to_download, pdf_dir)































































































