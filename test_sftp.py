#!/usr/bin/env python
"""
testSFTP.py: Python script to monitor SFTP site for connection issues
    * h_name: hostname for the site
    * u_name: username for the site
    * p_val: password for the site
    * s_dir: Location of test file
    * s_file: source location of test file
    * r_file: remote file name
"""

import signal
import logging
import configparser
import os
import pysftp as psftp
from pysftp.exceptions import ConnectionException
# import json
# from prtg.sensor.result import CustomSensorResult


class CheckSFTP:
    """ Class for verifying the connection for a given SFTP site """

    def __init__(self, h_name, u_name, p_val, f_name, s_dir):
        self.h_name = h_name
        self.u_name = u_name
        self.p_val = p_val
        self.f_name = f_name
        self.s_dir = s_dir
        self.check_sftp_conn()
        # self.csr = CustomSensorResult(text=self.h_name)

    def json_output(self, sftp_status):
        """ Function to store and display output"""
        # self.csr.add_primary_channel(channel_name="SFTP Status", value=sftp_status,
        #                             is_float=False)
        # print(self.csr.json_result)
        print(self.sftp_status)

    def handler(self, signum, frame):
        """ Timeout Function for the script """
        logging.info('Timed Out')
        self.sftp_status = 'Timed Out'
        self.json_output(self.sftp_status)
        raise SystemExit('Timed Out')

    def check_sftp_conn(self):
        """ Function to connect sftp site and test(get, put) operations """
        s_file = s_dir + self.f_name
        r_file = self.f_name
        cnopts = psftp.CnOpts()
        cnopts.hostkeys = None
        cinfo = {
            'host': self.h_name,
            'username': self.u_name,
            'password': self.p_val,
            'cnopts': cnopts
        }
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(60)
        try:
            with psftp.Connection(**cinfo) as sftp:
                logging.info('Connection successfully established...')
                logging.info("Listing directory for sftptest user (before deleting testfile): %s",
                             sftp.listdir())
                if sftp.exists(r_file):
                    logging.info('Cleaning testfile.')
                    sftp.remove(r_file)
                sftp.put(s_file, r_file)
                logging.info("Listing directory for sftptest user (after placing testfile): %s",
                             sftp.listdir())
                self.sftp_status = 'Connection Successful!'
                self.json_output(self.sftp_status)
        except ConnectionException as t_e:
            logging.error('%s: %s', type(t_e).__name__, str(t_e))
            self.sftp_status = 'Connection Failed!'
            self.json_output(self.sftp_status)


if __name__ == "__main__":
    s_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
    logging.basicConfig(filename=s_dir+'/test_sftp.log', filemode='w',
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO)
    config = configparser.ConfigParser()
    # i_csr = CustomSensorResult(text='Python Script Error')
    if os.path.isfile(s_dir + 'site.ini'):
        try:
            config.read("site.ini")
            h_name = config['DEFAULT']['host']
            u_name = config['DEFAULT']['username']
            p_val = config['DEFAULT']['password']
            f_name = config['DEFAULT']['test_file_name']
            c_sftp = CheckSFTP(h_name, u_name, p_val, f_name, s_dir)
        except KeyError as k:
            logging.error('%s: %s', type(k).__name__, str(k))
            # i_csr.add_primary_channel(channel_name="SFTP Status", value='Key Error(site.ini)',
            #                             is_float=False)
            # print(i_csr.json_result)
    else:
        logging.error('%s', 'site.ini not found!!')
        # i_csr.add_primary_channel(channel_name="SFTP Status", value='(File Not Found -- site.ini)',
        #                             is_float=False)
        # print(i_csr.json_result)
