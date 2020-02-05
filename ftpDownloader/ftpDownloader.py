# -*- coding: utf-8 -*-
# Author: Alexandre Correia / MARETEC
# Email: alexandre.c.correia@tecnico.ulisboa.pt
# Last update: 2002-01-31
#
# This script downloads files from a ftpserver, settings are read from a MOHID format .dat file.
# Python datetime codes are used to specify dates and times. (i.e. YYYY-MM-DD is %Y-%m-%d).
#
# Keywords:
# START : (str) date in YYYY MM DD HH MM SS format
# END : (str) date in YYYY MM DD HH MM SS format
# FTP_USERNAME : (str)(optional) username used to log in to ftp
# FTP_PASSWORD : (str)(optional) password used to log in to ftp
# FTP_HOST : (str) ftp host, don't include "ftp://" in this keyword
# FTP_DIR : (str) path to the working directory where the desired files are located, must start and 
# end with "/", use python datetime codes if the path changes with date and or time
# FTP_FILES_PREFIX : (str) the beggining of the desired files necessary to differentiate from other
# files in the working directory, use python datetime codes if the file name changes with date or
# time
# OUTPUT_DIR : (str) directory to save the files to

import os
from ftplib import FTP
from datetime import datetime, timedelta
from mohid_reader import mohid_dat_reader


def download_ftp_files(dat):

    print('Connecting to', dat['FTP_HOST'])
    # conecting to ftp host
    ftp = FTP(dat['FTP_HOST'])

    # if no user/password are provided attempts to login anonymously
    if ('FTP_USERNAME' in dat.keys()) and ('FTP_PASSWORD' in dat.keys()):
        print('Logging in with username: {} and respective password'.format(dat['FTP_USERNAME']))
        ftp.login(dat['FTP_USERNAME'], dat['FTP_PASSWORD'])
    else:
        print('Logging in with anonymous username')
        ftp.login()
    
    # defining first, last and currently downloading day for looping
    start_day = datetime(year=dat['START'].year, month=dat['START'].month, day=dat['START'].day)
    end_day = datetime(year=dat['END'].year, month=dat['END'].month, day=dat['END'].day)
    current_day = start_day

    # raises an error if 'END' date is before 'START' date
    if current_day > end_day:
        print('Starting date happens after End date, please see .dat file')
        exit(1)

    # gets the length of the defined FILE_PREFIX if it had a date written instead of datetime codes
    prefix_example = datetime.strftime(dat['START'], dat['FTP_FILES_PREFIX'])
    prefix_len = len(prefix_example)

    # downloading loop
    while current_day < end_day:
        # if 'FTP_DIR' has datetime codes translates them to strings
        if dat['FTP_DIR'].find('%') != -1:
            work_dir = current_day.strftime(dat['FTP_DIR'])
        else:
            work_dir = dat['FTP_DIR']
        # changes the working directory
        ftp.cwd(work_dir)
        # gets a list of all files in working directory
        files = ftp.nlst()
        # cycle through all files
        # when 'FTP_FILES_PREFIX' has datetime codes
        if dat['FTP_FILES_PREFIX'].find('%') != -1:
            for f in files:
                try:
                    # if this line raises a ValueError then the beggining of the file doesn't match
                    # the given 'FTP_FILES_PREFIX' and it doesn't download this file
                    f_day = datetime.strptime(f[:prefix_len], dat['FTP_FILES_PREFIX'])
                except ValueError:
                    continue
                if dat['START'] <= f_day < dat['END'] and not os.path.isfile(dat['OUTPUT_DIR']+f):
                    print('Downloading', f)
                    ftp.retrbinary('RETR {}'.format(f), open(dat['OUTPUT_DIR']+f, 'wb').write)
        else:
            for f in files:
                if f[:prefix_len] == f['FTP_FILES_PREFIX'] and not os.path.isfile(dat['OUTPUT_DIR']+f):
                    print('Downloading', f)
                    ftp.retrbinary('RETR {}'.format(f), open(dat['OUTPUT_DIR']+f, 'wb').write)

        current_day += timedelta(days=1)
    
    # closes the ftp connection
    ftp.quit()


def main():
    print('{:#^100}'.format(' Starting '+os.path.basename(__file__)+' ', fill='#'))
    dat = mohid_dat_reader.get_mohid_dat(os.path.basename(__file__).replace('.py','.dat'))
    download_ftp_files(dat)
    print('{:#^100}'.format(' Finished '+os.path.basename(__file__)+' sucessfully ', fill='#'))


if __name__ == '__main__':
    main()
