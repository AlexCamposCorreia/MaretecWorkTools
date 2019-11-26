from datetime import datetime


def process_keywords(key, value):
    if key == 'START' or key == 'END':
        try:
            value = datetime.strptime(value, '%Y %m %d %H %M %S')
        except ValueError:
            try:
                value = datetime.strptime(value, '%Y %m %d')
            except ValueError:
                print('Please use START and END in %Y %m %d %H %M %S or %Y %m %d format')
                exit(1)
    if key.find('DIR') != -1 and value.find('\\') != -1:
        value.replace('\\','/')
    if key.find('DIR') != -1 and not value.endswith('/'):
        value = value + '/'
    return key, value


def get_mohid_dat(file):
    f = open(file)
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
