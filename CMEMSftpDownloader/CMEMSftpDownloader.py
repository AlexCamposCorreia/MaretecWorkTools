import argparse
from ftplib import FTP
from datetime import datetime, timedelta
from mohid_reader import mohid_dat_reader


def download_CMEMS(dat):

    ftp = FTP(dat['FTP_HOST'])
    ftp.login(dat['COPERNICUS_USERNAME'], dat['COPERNICUS_PASSWORD'])
    
    current_date = dat['START']

    while (dat['END'] - current_date+timedelta(days=1)) > timedelta(0):
        print(current_date)
        year = datetime.strftime(current_date, '%Y')
        month = datetime.strftime(current_date, '%m')
        ftp.cwd(dat['FTP_DIR'] + '{}/{}/'.format(year, month))
        files = ftp.nlst()
        # this solution is not good, FIX LATER
        files = list(filter(lambda x: x.find(datetime.strftime(current_date, '%Y%m%d'))==33, files))
        if len(files) > 1:
            print('something went horribly wrong')
            exit(1)
        file = files[0]
        print('Downloading {} ...'.format(file))
        ftp.retrbinary('RETR {}'.format(file), open(dat['OUTPUT_DIR']+file, 'wb').write)
        current_date += timedelta(days=1)

    ftp.quit()


def main():
    dat = mohid_dat_reader.get_mohid_dat('CMEMSftpDownloader.dat')
    download_CMEMS(dat)


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
