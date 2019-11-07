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


def change_dates(dat):
    with open(dat['MOHID_XML_FILE'], 'r') as f:
        ls = f.readlines()

    f = open(dat['MOHID_XML_FILE'], 'w')
    for l in ls:
        if l.find('parameter') != -1 and l.find('"Start"') != -1:
            f.write(l[:l.find('value')+7]+datetime.strftime(dat['START'],'%Y %m %d %H %M %S'))
            l = l[l.find('value')+5:]
            l = l[l.find('"')+1:]
            l = l[l.find('"'):]
            f.write(l)
        elif l.find('parameter') != -1 and l.find('"End"') != -1:
            f.write(l[:l.find('value')+7]+datetime.strftime(dat['END'],'%Y %m %d %H %M %S'))
            l = l[l.find('value')+5:]
            l = l[l.find('"')+1:]
            l = l[l.find('"'):]
            f.write(l)
        else:
            f.write(l)

    f.close()


def main():
    dat = get_dat('ChangeMOHIDLagrangianDates.dat')
    change_dates(dat)


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
