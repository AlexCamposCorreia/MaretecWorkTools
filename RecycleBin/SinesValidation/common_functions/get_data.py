import numpy as np


def get_data(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.replace('\n','').split(',')
            try:
                line = [float(i) for i in line]
            except ValueError:
                print(line)
                input('Press enter to exit...')
                exit()
            
            try:
                arr = np.append(arr, [line], axis=0)
            except UnboundLocalError:
                arr = [line]
    return arr
