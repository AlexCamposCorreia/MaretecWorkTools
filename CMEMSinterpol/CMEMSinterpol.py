import os
from datetime import datetime, timedelta
from shutil import copy2, move
import subprocess
from mohid_reader import mohid_dat_reader


def clean_previous():
    try:
        os.remove('log.txt')
    except FileNotFoundError:
        pass
    try:
        os.remove('ConvertToHDF5Action_log.dat')
    except FileNotFoundError:
        pass


def download_files(dat):
    files = list(os.walk(dat['INPUT_DIR']))[0][2]
    files = list(filter(lambda x: x.startswith(dat['INPUT_NAME']), files))
    files = list(filter(lambda x: x.find('sub') == -1, files))
    files_list = []
    files_dates = []
    for file in files:
        file_date_str = file.replace(dat['INPUT_NAME']+'_','').replace('.hdf5','')
        file_date = datetime.strptime(file_date_str, '%Y%m%d%H')
        if dat['START']-timedelta(days=1) <= file_date <= dat['END']+timedelta(days=1):
            files_dates.append(file_date)
            copy2(dat['INPUT_DIR'] + file, './' + file)
            files_list.append('./' + file)
    return sorted(files_list), sorted(files_dates)


def write_ConvertToHDF5Action_log(filepath):
    f1 = open(filepath, 'r')
    f2 = open('ConvertToHDF5Action_log.dat', 'a')

    while True:
        l = f1.readline()
        if l == '':
            break
        f2.write(l)
    f2.write('-'*120+'\n')
    f1.close()
    f2.close()


def translate_INTERPOLATE_GRIDS(dat, date):
    f1 = open(dat['INTERPOLATE_GRIDS_TEMPLATE'], 'r')
    f2 = open('ConvertToHDF5Action.dat', 'w')

    outputfilename = './'+dat['OUTPUT_NAME']+'_'+datetime.strftime(date,'%Y%m%d%H')+'.hdf5'

    while True:
        l = f1.readline()
        if l == '':
            break
        if l.startswith('!'):
            continue
        if l.find('!') != -1:
            l = l[:l.find(':')]
        if l.strip().startswith('FATHER_FILENAME'):
            f2.write('{0:30}{1}'.format('FATHER_FILENAME', ': ' + './'+dat['INPUT_NAME']+'_'+datetime.strftime(date,'%Y%m%d%H')+'.hdf5'+'\n'))
        elif l.strip().startswith('OUTPUTFILENAME'):
            f2.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' + outputfilename+'\n'))
        elif l.strip().startswith('START'):
            f2.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(date,'%Y %m %d %H %M %S')+'\n'))
        elif l.strip().startswith('END'):
            f2.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(date,'%Y %m %d %H %M %S')+'\n'))
        else:
            f2.write(l)
    f1.close()
    f2.close()
    write_ConvertToHDF5Action_log('ConvertToHDF5Action.dat')
    return outputfilename


def translate_GLUES_HDF5_FILES(dat, files, start, end):
    f1 = open(dat['GLUES_HDF5_FILES_TEMPLATE'], 'r')
    f2 = open('ConvertToHDF5Action.dat', 'w')

    outputfilename = './'+dat['OUTPUT_NAME']+'_'+datetime.strftime(dat['START'],'%Y-%m-%d')+\
        '_'+datetime.strftime(dat['END'],'%Y-%m-%d')+'.hdf5'

    while True:
        l = f1.readline()
        if l == '':
            break
        if l.startswith('!'):
            continue
        if l.find('!') != -1:
            l = l[:l.find(':')]
        if l.strip().startswith('OUTPUTFILENAME'):
            f2.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' + outputfilename +'\n'))
        elif l.strip().startswith('START'):
            f2.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(start,'%Y %m %d %H %M %S')+'\n'))
        elif l.strip().startswith('END'):
            f2.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(end,'%Y %m %d %H %M %S')+'\n'))
        elif l.strip().startswith('<<begin_list>>'):
            f2.write('<<begin_list>>\n')
            for file in files:
                f2.write(file+'\n')
        else:
            f2.write(l)

    f1.close()
    f2.close()
    write_ConvertToHDF5Action_log('ConvertToHDF5Action.dat')
    return outputfilename


def run_ConvertToHDF5(dat):
    with open('log.txt', 'a') as logfile:
        p = subprocess.Popen(dat['CONVERTTOHDF5_EXE'], stdout=logfile, stderr=logfile)
        p.wait()


def move_output(dat, outputfilename):
    move(outputfilename, './History/'+outputfilename)


def clean(files):
    for file in files:
        os.remove(file)


def main():
    clean_previous()
    dat = mohid_dat_reader.get_mohid_dat('CMEMSinterpol.dat')
    downloaded_files, files_dates = download_files(dat)
    interpolated_files = []
    for date in files_dates:
        interpolated_file = translate_INTERPOLATE_GRIDS(dat, date)
        interpolated_files.append(interpolated_file)
        run_ConvertToHDF5(dat)
    outputfilename = translate_GLUES_HDF5_FILES(dat, interpolated_files, files_dates[0], files_dates[1])
    run_ConvertToHDF5(dat)
    move_output(dat, outputfilename)
    clean(downloaded_files + interpolated_files)


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
