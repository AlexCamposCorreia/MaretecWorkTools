import os

from common_functions.campaign import CampaignPlotter


if __name__ == '__main__':

    model_profiles_loc = './model_results/profiles'
    obs_profiles_loc = './insitu'

    dirs = next(os.walk('.'))[1]
    cp_dirs = list(filter(lambda x: x.startswith('campanha'), dirs))

    for cp_dir in cp_dirs:
        print('\n\n'+cp_dir)
        os.chdir(cp_dir)
        a = CampaignPlotter(model_profiles_loc, obs_profiles_loc)
        for prop in a.get_mutual_properties():
            a.plot_property(prop)
            #a.plot_property_error(prop)

        os.chdir('..')
