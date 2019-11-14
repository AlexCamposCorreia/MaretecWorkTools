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


def check_existing_file(yaml, start, end):
    return os.path.isfile('./History/'+yaml['getMeteoPy']['meteoModel']+'_'+yaml['getMeteoPy']['domainName']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5')


def copy_meteo_files(yaml, meteoModel, start, end):
    # copies meteo hdf5 files in the format ModelName_YYYYMMDDHH_YYYYMMDDHH.hdf5
    hdf5_files_copied = []
    hdf5_files = list(filter(lambda x: x.endswith('.hdf5'), list(os.walk(yaml['getMeteoPy']['meteoModels'][meteoModel]['meteoDirectory']))[0][2]))
    hdf5_files = list(filter(lambda x: x.startswith(yaml['getMeteoPy']['meteoModels'][meteoModel]['meteoName']), hdf5_files))
    hdf5_files = list(filter(lambda x: not x.endswith('Copy.hdf5'), hdf5_files))
    hdf5_files_useful = []
    for hdf5_file in hdf5_files:
        date = hdf5_file.split('_')[-1].replace('.hdf5','')
        date = datetime.strptime(date, '%Y%m%d%H')
        if start-timedelta(days=3)  <= date < end-timedelta(days=1):
            hdf5_files_useful.append(yaml['getMeteoPy']['meteoModels'][meteoModel]['meteoDirectory']+hdf5_file)
    hdf5_files_useful = sorted(hdf5_files_useful)
    print(hdf5_files_useful[-1])
    copy2(hdf5_files_useful[-1], './')
    hdf5_files_copied.append(hdf5_files_useful[-1].replace(yaml['getMeteoPy']['meteoModels'][meteoModel]['meteoDirectory'],''))
    return sorted(hdf5_files_copied)


def write_ConvertToHDF5Action_glue(yaml, meteoModel, start, end, files_to_glue):
    with open('./ConvertToHDF5Action.dat', 'w') as f:
        f.write('<begin_file>\n')
        f.write('\n')
        f.write('{0:30}{1}'.format('ACTION', ': ' + 'GLUES HDF5 FILES' + '\n'))
        f.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' + yaml['getMeteoPy']['meteoModels'][meteoModel]['meteoName']+'.hdf5' + '\n'))
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
        for meteoModel in yaml['getMeteoPy']['meteoModels'].keys():
            meteoModel = yaml['getMeteoPy']['meteoModels'][meteoModel]
            f.write('{0:30}{1}'.format('FATHER_FILENAME', ': ' + meteoModel['meteoName']+'.hdf5' + '\n'))
            f.write('{0:30}{1}'.format('FATHER_GRID_FILENAME', ': ' + meteoModel['meteoName']+'.dat' + '\n'))
        f.write('\n')
        f.write('<<BeginFields>>\n')
        for p in yaml['getMeteoPy']['propertiesToInterpolate']:
            f.write(p+'\n')
        f.write('<<EndFields>>\n')
        f.write('\n')
        f.write('<end_file>\n')
    copy2('./ConvertToHDF5Action.dat', './ConvertToHDF5Action-INTERPOLATE_GRIDS.dat')


def write_ConvertToHDF5Action_patch(yaml, start, end):
    with open('./ConvertToHDF5Action.dat', 'w') as f:
        f.write('<begin_file>\n')
        f.write('\n')
        f.write('{0:30}{1}'.format('ACTION', ': ' + 'PATCH HDF5 FILES' + '\n'))
        f.write('{0:30}{1}'.format('TYPE_OF_INTERPOLATION', ': ' + '3' + '\n'))
        f.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' +
                yaml['getMeteoPy']['meteoModel']+'_'+yaml['getMeteoPy']['domainName']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5' + '\n'))
        f.write('{0:30}{1}'.format('NEW_GRID_FILENAME', ': ' + yaml['getMeteoPy']['bathymetry'] + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(start, '%Y %m %d %H %M %S') + '\n'))
        f.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(end, '%Y %m %d %H %M %S') + '\n'))
        f.write('\n')
        for meteoModel in yaml['getMeteoPy']['meteoModels'].keys():
            meteoModel = yaml['getMeteoPy']['meteoModels'][meteoModel]
            f.write('<<begin_father>>\n')
            f.write('{0:30}{1}'.format('FATHER_FILENAME', ': ' + meteoModel['meteoName']+'.hdf5' + '\n'))
            f.write('{0:30}{1}'.format('FATHER_GRID_FILENAME', ': ' + meteoModel['meteoName']+'.dat' + '\n'))
            f.write('{0:30}{1}'.format('LEVEL', ': ' + str(meteoModel['level']) + '\n'))
            f.write('<<end_father>>\n')
        f.write('\n')
        f.write('<<BeginFields>>\n')
        for p in yaml['getMeteoPy']['propertiesToInterpolate']:
            f.write(p+'\n')
        f.write('<<EndFields>>\n')
        f.write('\n')
        f.write('<end_file>\n')
    copy2('./ConvertToHDF5Action.dat', './ConvertToHDF5Action-PATCH_HDF5_FILES.dat')


def move_interpolated_hdf5_to_History_folder(yaml, start, end):
    move(yaml['getMeteoPy']['meteoModel']+'_'+yaml['getMeteoPy']['domainName']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5',
        yaml['getMeteoPy']['outputDir']+yaml['getMeteoPy']['meteoModel']+'_'+yaml['getMeteoPy']['domainName']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5')


def delete_copied_and_created_files(yaml, hdf5_files_to_delete):
    for meteoModel in yaml['getMeteoPy']['meteoModels'].keys():
        try:
            meteoModel = yaml['getMeteoPy']['meteoModels'][meteoModel]
            os.remove(meteoModel['meteoName']+'.hdf5')
        except FileNotFoundError:
            pass
    os.remove('ConvertToHDF5Action.dat')
    for f in hdf5_files_to_delete:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass




def main():
    
    yaml = open_yaml_file('GetMeteoPy.yaml')
    start, end = get_start_and_end('./GetMeteoPy.dat')
    
    if os.path.isdir('./History') is False:
        os.mkdir('./History')

    if 'dontRunIfFileExists' in yaml['getMeteoPy'].keys():
        if yaml['getMeteoPy']['dontRunIfFileExists'] and check_existing_file(yaml, start, end):
            print('Requested day already in History directory, ignoring')
            exit(0)

    hdf5_files_to_delete = []
    # copy and glue
    for meteoModel in yaml['getMeteoPy']['meteoModels'].keys():
        hdf5_files_copied = copy_meteo_files(yaml, meteoModel, start, end)
        hdf5_files_to_delete += hdf5_files_copied
        if len(hdf5_files_copied) == 1:
            move(hdf5_files_copied[0], yaml['getMeteoPy']['meteoModels'][meteoModel]['meteoName']+'.hdf5')
        elif len(hdf5_files_copied) >1:
            write_ConvertToHDF5Action_glue(yaml, meteoModel, start, end, hdf5_files_copied)
            with open('glue_log.txt', 'w') as logfile:
                p = subprocess.Popen(yaml['getMeteoPy']['convertToHDF5exe'], stdout=logfile, stderr=logfile)
                p.wait()
    
    # interpolate
    if len(yaml['getMeteoPy']['meteoModels'].keys()) == 1:
        write_ConvertToHDF5Action_interpolate(yaml, start, end)
        with open('interpolation_log.txt', 'w') as logfile:
            p = subprocess.Popen(yaml['getMeteoPy']['convertToHDF5exe'], stdout=logfile, stderr=logfile)
            p.wait()
        move_interpolated_hdf5_to_History_folder(yaml, start, end)
    # patch
    elif len(yaml['getMeteoPy']['meteoModels'].keys()) > 1:
        write_ConvertToHDF5Action_patch(yaml, start, end)
        with open('patch_log.txt', 'w') as logfile:
            p = subprocess.Popen(yaml['getMeteoPy']['convertToHDF5exe'], stdout=logfile, stderr=logfile)
            p.wait()
        move_interpolated_hdf5_to_History_folder(yaml, start, end)
    # cleanup
    delete_copied_and_created_files(yaml, hdf5_files_to_delete)
    



if __name__ == '__main__':
    main()
