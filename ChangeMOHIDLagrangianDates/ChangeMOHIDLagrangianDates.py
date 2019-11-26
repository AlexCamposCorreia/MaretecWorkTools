from datetime import datetime
from mohid_reader import mohid_dat_reader


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
    dat = mohid_dat_reader.get_mohid_dat('ChangeMOHIDLagrangianDates.dat')
    change_dates(dat)


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
