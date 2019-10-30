# -*- coding: utf-8 -*-

import numpy as np
from scipy import interpolate, stats
from math import sqrt
import os
import sys
from calculate_salinity import calculate_model_salinities

scenario = sys.argv[1]

MODEL_PROFILES_LOCATION = './{}/profiles/'.format(scenario)
CAMPAIGN_PROFILES_LOCATION = './campaign/'
GRAPHS_OUTPUT_LOCATION = './output/'

def get_data(filename):
    with open(filename) as f:
        for line in f:
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

def statistics_indicators(arr_camp, arr_mod):
    if arr_camp[0,1] > arr_mod[0,1]:
        print('Profundidade do primeiro ponto da campanha mais alto que o \
        primeiro ponto do modelo. Este caso especifico ainda não está \
        programado no script.')
        input('Press the ENTER key to continue...')
        
    ### Interpolação dos valores:
    interp_Ts = []
    n = 1
    for depth in arr_camp[:,1]:
        

        while True:
            if depth > arr_mod[0,1]:
                break
            elif depth < arr_mod[-1,1]:
                # quando a depth é mais baixa que o ultimo valor da
                # profundidade do modelo os valores são extrapolados
                value = arr_mod[-2,0] + (depth-arr_mod[-2,1]) * \
                (arr_mod[-2,0]-arr_mod[n,0])/(arr_mod[n-1,1]-arr_mod[n,1])
                interp_Ts.append(value)
                break
            elif arr_mod[n-1,1] >= depth >= arr_mod[n,1]:
                # quando a depth é mais baixa que n-1 e mais alta que n
                # interpola o valor
                value = arr_mod[n-1,0] + (depth-arr_mod[n-1,1]) * \
                (arr_mod[n-1,0]-arr_mod[n,0])/(arr_mod[n-1,1]-arr_mod[n,1])
                interp_Ts.append(value)
                break
            elif depth < arr_mod[n,1]:
                # se a depth for mais baixa que n então aumenta o n
                n += 1

    
    ### Calcula, pearson, RMSE e o bias:
    RMSE = 0
    max_error = 0
    for n in range(0,len(interp_Ts)):
        sqr_error = (interp_Ts[n]- arr_camp[n,0])**2
        max_error = sqrt(sqr_error) if sqrt(sqr_error) > max_error else max_error
        RMSE += sqr_error
    RMSE = sqrt(RMSE / len(interp_Ts))
    
    bias = np.mean(interp_Ts) - np.mean(arr_camp[:,0])

    pearson, p_value = stats.pearsonr(interp_Ts, arr_camp[:,0])

    return round(RMSE,3), round(bias,3), round(pearson,3), round(max_error,3), interp_Ts


def main(filename, csvfile):

    c = ','

    try:
        arr_camp_CTD = get_data(CAMPAIGN_PROFILES_LOCATION+'CTD/'+filename)
    except FileNotFoundError:
        arr_camp_CTD = None

    try:
        arr_camp_Sonda = get_data(CAMPAIGN_PROFILES_LOCATION+'Sonda/'+filename)
    except FileNotFoundError:
        arr_camp_Sonda = None

    arr_mod = get_data(MODEL_PROFILES_LOCATION+filename)

    if arr_camp_CTD is not None:
        RMSE, bias, pearson, max_error, interp = statistics_indicators(arr_camp_CTD, arr_mod)
        print('modelo e CTD')
        print(RMSE, bias, pearson, max_error)
        aux = ['PCOMS', 'MM5', 'CTD', RMSE, bias, pearson, max_error]
        aux = [str(x) for x in aux]
        aux = [filename.replace('.csv','')] + aux
        csvfile.write(c.join(aux)+'\n')
        np.savetxt(GRAPHS_OUTPUT_LOCATION + scenario + '.' + filename, interp, delimiter=',')

    if (arr_camp_Sonda is not None) and (arr_camp_CTD is None):
        RMSE, bias, pearson, max_error, interp = statistics_indicators(arr_camp_Sonda, arr_mod)
        print('modelo e Sonda')
        print(RMSE, bias, pearson, max_error)
        aux = ['PCOMS', 'MM5', 'Sonda', RMSE, bias, pearson, max_error]
        aux = [str(x) for x in aux]
        aux = [filename.replace('.csv','')] + aux
        csvfile.write(c.join(aux)+'\n')

    print()
# ------------------------------------------------------------------------------

if __name__ == '__main__':

    property_names = ['Temperatura', 'Salinidade', 'Densidade']

    stations = ['S1', 'S2A', 'S3', 'S5']

    calculate_model_salinities(MODEL_PROFILES_LOCATION, stations)

    csvfile = open(GRAPHS_OUTPUT_LOCATION+scenario+'.statistics.csv', 'w')
    aux = ['propriedade', 'modelo pai', 'modelo atm.', 'aparelho', 'RMSE', 'BE', 'Pearson r', 'max error']
    csvfile.write(','.join(aux)+'\n')

    for property_name in property_names:

        filenames = []
        for station in stations:
            filename = property_name + station + '.csv'
            print(filename)
            main(filename, csvfile)

    csvfile.close()

    print('Finished Successfuly')
