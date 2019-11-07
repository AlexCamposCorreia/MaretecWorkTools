import os
import subprocess
from datetime import datetime


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


def clean():
    for f in next(os.walk('./input'))[1]:
        os.remove(f)
    try: os.remove('./pallete.png')
    except FileNotFoundError: pass


def main(dat):
    import ParaView_Images
    cmd = './ffmpeg/ffmpeg.exe -f image2 -i ./input/anim.%04d.png -vf palettegen palette.png'
    with open('log.txt', 'a') as logfile:
        p = subprocess.Popen(cmd, stdout=logfile, stderr=logfile)
        p.wait()
    cmd = './ffmpeg/ffmpeg.exe -f image2 -framerate 10 -i ./input/anim.%04d.png -i palette.png -filter_complex "scale=493:536[x];[x][1:v]paletteuse" ./output/anim_{}.gif'.format(
        datetime.strftime(dat['START'],'%Y-%m-%d')+'_'+datetime.strftime(dat['END'],'%Y-%m-%d'))
    with open('log.txt', 'a') as logfile:
        p = subprocess.Popen(cmd, stdout=logfile, stderr=logfile)
        p.wait()
    

if __name__ == '__main__':
    dat = get_dat('PRIMROSEanimations.dat')
    clean()
    main(dat)
