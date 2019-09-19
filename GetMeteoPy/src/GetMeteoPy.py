import os
import sys
import subprocess
from shutil import copy2, move
from datetime import datetime, timedelta
import yaml


def open_yaml_file(path):
    with open(path, 'r') as yml_file:
        return yaml.safe_load(yml_file)

def get_start_and_end(path):
    with open(path, 'r') as f:
        all_lines = f.readlines()
        all_lines = list(map(lambda x: x.replace('\n',''), all_lines))
        all_lines = list(filter(lambda x: len(x)>0, all_lines))
        for line in all_lines:
            if line.find('START') > -1:
                start = line[line.find(':')+1:].strip(' ')
            if line.find('END') > -1:
                end = line[line.find(':')+1:].strip(' ')

    try:
        start = datetime.strptime(start, '%Y %m %d %H %M %S')
        end = datetime.strptime(end, '%Y %m %d %H %M %S')
    except ValueError:
        start = datetime.strptime(start, '%Y %m %d')
        end = datetime.strptime(end, '%Y %m %d')
    return start, end




def copy_meteo_files(yaml, start, end):
    hdf5_files = list(filter(lambda x: x.endswith('.hdf5'), list(os.walk(yaml['getMeteoPy']['meteoDirectory']))[0][2]))
    hdf5_files = list(filter(lambda x: x.startswith(yaml['getMeteoPy']['meteoName']), hdf5_files))
    hdf5_files = list(filter(lambda x: not x.endswith('Copy.hdf5'), hdf5_files))
    hdf5_files_copied = []
    copied_dat_file = False
    for hdf5_file in hdf5_files:
        dates = hdf5_file[-26:-5]
        dates = dates.split('_')
        dates = [datetime.strptime(x, '%Y%m%d%H') for x in dates]
        if start <= dates[0] <= end or start <= dates[1] <= end:
            if copied_dat_file is False:
                    copy2(yaml['getMeteoPy']['meteoDirectory']+hdf5_file.replace('.hdf5','.dat'),
                        './'+hdf5_file.replace('.hdf5','.dat')[:-26] + hdf5_file.replace('.hdf5','.dat')[-4:]) 
                    copied_dat_file = True
            copy2(yaml['getMeteoPy']['meteoDirectory'] + hdf5_file, './')
            hdf5_files_copied.append(hdf5_file)
    return sorted(hdf5_files_copied)

def write_ConvertToHDF5Action_glue(yaml, start, end, files_to_glue):
    with open('./ConvertToHDF5Action.dat', 'w') as f:
        f.write('<begin_file>\n')
        f.write('\n')
        f.write('{0:30}{1}'.format('ACTION', ': ' + 'GLUES HDF5 FILES' + '\n'))
        f.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' + yaml['getMeteoPy']['meteoName']+'.hdf5' + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(start, '%Y %m %d %H %M %S') + '\n'))
        f.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(end, '%Y %m %d %H %M %S') + '\n'))
        f.write('\n')
        f.write('<<begin_list>>\n')
        for hdf5_file in files_to_glue:
            f.write(hdf5_file+'\n')
        f.write('<<end_list>>\n')
        f.write('\n')
        f.write('<end_file>\n')
    copy2('./ConvertToHDF5Action.dat', './ConvertToHDF5Action-GLUES_HDF5_FILES.dat')

def write_ConvertToHDF5Action_interpolate(yaml, start, end):
    with open('./ConvertToHDF5Action.dat', 'w') as f:
        f.write('<begin_file>\n')
        f.write('\n')
        f.write('{0:30}{1}'.format('ACTION', ': ' + 'INTERPOLATE GRIDS' + '\n'))
        f.write('{0:30}{1}'.format('TYPE_OF_INTERPOLATION', ': ' + '3' + '\n'))
        f.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' +
                yaml['getMeteoPy']['meteoModel']+'_'+yaml['getMeteoPy']['domainName']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5' + '\n'))
        f.write('{0:30}{1}'.format('NEW_GRID_FILENAME', ': ' + yaml['getMeteoPy']['bathymetry'] + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(start, '%Y %m %d %H %M %S') + '\n'))
        f.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(end, '%Y %m %d %H %M %S') + '\n'))
        f.write('\n')
        f.write('<<begin_father>>\n')
        f.write('{0:30}{1}'.format('FATHER_FILENAME', ': ' + yaml['getMeteoPy']['meteoName']+'.hdf5' + '\n'))
        f.write('{0:30}{1}'.format('FATHER_GRID_FILENAME', ': ' + yaml['getMeteoPy']['meteoName']+'.dat' + '\n'))
        f.write('<<end_father>>\n')
        f.write('\n')
        f.write('<<BeginFields>>\n')
        for p in yaml['getMeteoPy']['propertiesToInterpolate']:
            f.write(p+'\n')
        f.write('<<EndFields>>\n')
        f.write('\n')
        f.write('<end_file>\n')
    copy2('./ConvertToHDF5Action.dat', './ConvertToHDF5Action-INTERPOLATE_GRIDS.dat')

def move_interpolated_hdf5_to_History_folder(yaml, start, end):
    move(yaml['getMeteoPy']['meteoModel']+'_'+yaml['getMeteoPy']['domainName']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5',
        './History/'+yaml['getMeteoPy']['meteoModel']+'_'+yaml['getMeteoPy']['domainName']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5')

def delete_copied_and_created_files(yaml, hdf5_files_copied):
    os.remove(yaml['getMeteoPy']['meteoName']+'.hdf5')
    os.remove(yaml['getMeteoPy']['meteoName']+'.dat')
    os.remove('ConvertToHDF5Action.dat')
    for f in hdf5_files_copied:
        os.remove(f)




def main():
    yaml = open_yaml_file('GetMeteoPy.yaml')
    start, end = get_start_and_end('./GetMeteoPy.dat')
    hdf5_files_copied = copy_meteo_files(yaml, start, end)
    write_ConvertToHDF5Action_glue(yaml, start, end, hdf5_files_copied)
    with open('glue_log.txt', 'w') as logfile:
        p = subprocess.Popen('ConvertToHDF5.exe', stdout=logfile, stderr=logfile)
        p.wait()
    write_ConvertToHDF5Action_interpolate(yaml, start, end)
    with open('interpolation_log.txt', 'w') as logfile:
        p = subprocess.Popen('ConvertToHDF5.exe', stdout=logfile, stderr=logfile)
        p.wait()
    move_interpolated_hdf5_to_History_folder(yaml, start, end)
    delete_copied_and_created_files(yaml, hdf5_files_copied)



if __name__ == '__main__':
    main()
