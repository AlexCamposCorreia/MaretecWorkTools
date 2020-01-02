import os
from sklearn.metrics import mean_squared_error

import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats



from common_functions.campaign import Campaign


if __name__ == '__main__':

    mlp.rcParams['lines.linewidth'] = 1
    mlp.rcParams['lines.markersize'] = 1.5
    mlp.rcParams['font.size'] = 6
    mlp.rcParams['xtick.labelsize'] = 5
    mlp.rcParams['ytick.labelsize'] = 5


    f = open('global_statistics.csv', 'w')
    f.write('Property,RMSE,Bias,r\n')
    dirs = next(os.walk('.'))[1]
    cp_dirs = list(filter(lambda x: x.startswith('campanha'), dirs))
    possible_properties = []

    for cp_dir in cp_dirs:
        model_profiles_location = cp_dir + '/model_results/profiles'
        obs_profiles_location = cp_dir + '/insitu'

        a = Campaign(model_profiles_location, obs_profiles_location)
        for p in a.mutual_properties:
            possible_properties.append(p)

    possible_properties = list(dict.fromkeys(possible_properties))



    for prop_name in possible_properties:
        fig, ax = plt.subplots(1,1)

        ax.set_title(prop_name)
        ax.set_xlabel('Observations')
        ax.set_ylabel('Model')

        min_value = 1e+99
        max_value = 1e-99

        colors = ['blue', 'green', 'red', 'orange', 'black', 'brown' 'pruple']
        colors = ['red', 'orange', 'green', 'blue', 'purple', 'brown', 'black']

        color_index = 0

        all_obs_values = []
        all_model_values = []
        
        for cp_dir in cp_dirs:
            model_profiles_location = cp_dir + '/model_results/profiles'
            obs_profiles_location = cp_dir + '/insitu'
            a = Campaign(model_profiles_location, obs_profiles_location)

            for s in a.stations:
                try:
                    obs_arr, model_arr = a.get_cut_obs_and_model_interpolated_to_obs_depth(prop_name, s)
                    all_obs_values = np.append(all_obs_values, obs_arr[:,1], axis=0)
                    all_model_values = np.append(all_model_values, model_arr[:,1], axis=0)
                    min_value = np.min([min_value, np.min([np.min(obs_arr[:,1]), np.min(model_arr[:,1])])])
                    max_value = np.max([max_value, np.max([np.max(obs_arr[:,1]), np.max(model_arr[:,1])])])
                    if s == 'S1':
                        ax.scatter(obs_arr[:,1], model_arr[:,1], c=colors[color_index], label=cp_dir)
                except FileNotFoundError:
                    print("Didn't find {} {}{}".format(cp_dir, prop_name, s))
                except TypeError:
                    print("Didn't find {} {}{}".format(cp_dir, prop_name, s))
        
            color_index += 1

        ax.legend()
        ax.plot([0, 99999], [0, 99999], linewidth=0.5, c='black', linestyle='dashed')
        ax.set_xlim(min_value - 0.1*(max_value-min_value), max_value + 0.1*(max_value-min_value))
        ax.set_ylim(min_value - 0.1*(max_value-min_value), max_value + 0.1*(max_value-min_value))
        print(min_value, max_value)

        #ax.plot([min_value, min_value], [max_value, max_value], linewidth=0.5, c='black', linestyle='dashed')
        figname = './comparison/' + prop_name + '.pdf'
        fig.savefig(figname)
        plt.close(fig=fig)

        RMSE = np.sqrt(mean_squared_error(all_obs_values, all_model_values))
        BIAS = np.mean(all_obs_values) - np.mean(all_model_values)
        Pearson = stats.pearsonr(all_obs_values, all_model_values)[0]

        f.write('{},{},{},{}\n'.format(prop_name, str(RMSE), str(BIAS), str(Pearson)))
    f.close()
