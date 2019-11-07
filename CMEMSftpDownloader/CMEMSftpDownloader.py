import argparse
from ftplib import FTP
from datetime import datetime, timedelta


def process_keywords(key, value):
    if key == 'START' or key == 'END':
        value = datetime.strptime(value, '%Y %m %d %H %M %S')
    if key.find('DIR') != -1 and value.find('\\') != -1:
        value.replace('\\','/')
    if key.find('DIR') != -1 and not value.endswith('/'):
        value = value + '/'
    return key, value


def get_dat(path):
    f = open(path)
    dat = {}
    while True:
        l = f.readline()
        if l == '':
            break
        if l.startswith('!'):
            continue
        if l.find('!') != -1:
            l = l[:l.find('!')]
        if l.find(':') != -1:
            key = l[:l.find(':')]
            value = l[l.find(':')+1:]
            key = key.strip(' \n')
            value = value.strip(' \n')
            key = key.upper()
            key, value = process_keywords(key, value)
            dat.update({key: value})
    f.close()
    return dat


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
    dat = get_dat('CMEMSftpDownloader.dat')
    download_CMEMS(dat)


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
