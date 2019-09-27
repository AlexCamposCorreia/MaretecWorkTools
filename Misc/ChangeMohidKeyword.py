import sys


def change_mohid_keyword(file_to_change, keyword_to_change, new_value):
    with open(file_to_change, 'r') as f:
        f_old = f.readlines()

    with open(file_to_change, 'w') as f_new:
        for l in f_old:
            if l.strip(' ').startswith(keyword_to_change):
                f_new.write(l[:l.find(':')+1] + ' ' + new_value + '\n')
            else:
                f_new.write(l)

if __name__ == '__main__':
    file_to_change = sys.argv[1]
    keyword_to_change = sys.argv[2]
    new_value = sys.argv[3]
    change_mohid_keyword(file_to_change, keyword_to_change, new_value)