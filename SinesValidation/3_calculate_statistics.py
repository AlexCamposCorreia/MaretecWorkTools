import os

from common_functions.campaign import Campaign


if __name__ == '__main__':
    model_profiles_loc = './model_results/profiles'
    obs_profiles_loc = './insitu'
    decimal_separator = ','

    dirs = next(os.walk('.'))[1]
    cp_dirs = list(filter(lambda x: x.startswith('campanha'), dirs))

    for cp_dir in cp_dirs:
        print('\n\n'+cp_dir)
        os.chdir(cp_dir)
        a = Campaign(model_profiles_loc, obs_profiles_loc)

        with open('./statistics.csv', 'w') as f:
            f.write('property_name{0}station{0}RMSE{0}Bias{0}r\n'.format(decimal_separator))
            for p_name in a.mutual_properties:
                for s in a.stations:
                    f.write('{1}{0}{2}{0}{3}{0}{4}{0}{5}\n'.format(
                        decimal_separator, p_name, s,
                        a.get_RMSE(p_name, s),
                        a.get_bias(p_name, s),
                        a.get_pearson_correlation(p_name, s)))

        os.chdir('..')
