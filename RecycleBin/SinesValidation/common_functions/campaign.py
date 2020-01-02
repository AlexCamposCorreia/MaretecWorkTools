import os
from datetime import datetime

import numpy as np
from sklearn.metrics import mean_squared_error
from scipy import stats
import matplotlib as mlp
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from common_functions.get_data import get_data
from common_functions.interpolate_model_to_obs_depths import interpolate_model_to_obs_depths


### AUX FUNCTIONS #############################################################
def cut_station(x):
    stations = ['S1.csv','S2.csv','S2A.csv','S3.csv','S4.csv','S5.csv']
    for s in stations:
        x = x.replace(s, '')
    return x
###############################################################################


### CLASSES ###################################################################
class Campaign():

    def __init__(self, model_profiles_location, obs_profiles_location):
        self.model_profiles_location = model_profiles_location
        self.obs_profile_location = obs_profiles_location

        self.available_model_properties = list(dict.fromkeys([cut_station(x) for x in next(os.walk(model_profiles_location))[2]]))

        self.available_obs_properties = []
        if list(os.walk(obs_profiles_location+'/CTD')):
            self.available_obs_properties += next(os.walk(obs_profiles_location+'/CTD'))[2]
        if list(os.walk(obs_profiles_location+'/sonda')):
            self.available_obs_properties += next(os.walk(obs_profiles_location+'/sonda'))[2]
        if list(os.walk(obs_profiles_location+'/velocities')):
            self.available_obs_properties += next(os.walk(obs_profiles_location+'/velocities'))[2]
        self.available_obs_properties = list(dict.fromkeys([cut_station(x) for x in self.available_obs_properties]))

        self.mutual_properties = [x for x in list(dict.fromkeys(self.available_model_properties + self.available_obs_properties)) \
            if x in self.available_model_properties and x in self.available_obs_properties]

        aux = obs_profiles_location.replace('/insitu', '/model_results/Sines4/Results_HDF')
        aux = list(next(os.walk(aux)))[1][0][:10]
        self.date = datetime.strptime(aux, '%Y-%m-%d')

        self.stations = [x.replace('temperature','').replace('.csv','') for x in list(next(os.walk(model_profiles_location))[2]) if x.startswith('temperature')]

    def get_mutual_properties(self):
        return self.mutual_properties
    
    def get_date(self):
        return self.date
    
    def get_date_string(self):
        return datetime.strftime(self.date, '%Y-%m-%d')
    
    def get_model_prop_arr(self, property_name, station):
        if property_name.find('velocity modulus') > -1:
            return get_data(self.model_profiles_location+'/'+property_name)
        return get_data(self.model_profiles_location+'/'+property_name+station+'.csv')

    def get_obs_CTD_prop_arr(self, property_name, station):
        return get_data(self.obs_profile_location+'/CTD/'+property_name+station+'.csv')

    def get_obs_sonda_prop_arr(self, property_name, station):
        return get_data(self.obs_profile_location+'/sonda/'+property_name+station+'.csv')
    
    def get_best_obs_prop_arr(self, property_name, station):
        try:
            return get_data(self.obs_profile_location+'/CTD/'+property_name+station+'.csv')
        except FileNotFoundError:
            try:
                return get_data(self.obs_profile_location+'/sonda/'+property_name+station+'.csv')
            except FileNotFoundError:
                print("Didn't find CTD or sonda file for {}, returning None".format(property_name+station+'.csv'))
                return None

    def get_cut_obs_and_model_interpolated_to_obs_depth(self, property_name, station):
        model_arr = get_data(self.model_profiles_location+'/'+property_name+station+'.csv')
        obs_arr = self.get_best_obs_prop_arr(property_name, station)
        return interpolate_model_to_obs_depths(model_arr, obs_arr)

    def get_RMSE(self, property_name, station):
        cut_obs_arr, interp_model_arr = self.get_cut_obs_and_model_interpolated_to_obs_depth(property_name, station)
        return np.sqrt(mean_squared_error(cut_obs_arr[:,1], interp_model_arr[:,1]))

    def get_bias(self, property_name, station):
        cut_obs_arr, interp_model_arr = self.get_cut_obs_and_model_interpolated_to_obs_depth(property_name, station)
        return np.mean(cut_obs_arr[:,1]) - np.mean(interp_model_arr[:,1])
    
    def get_pearson_correlation(self, property_name, station):
        cut_obs_arr, interp_model_arr = self.get_cut_obs_and_model_interpolated_to_obs_depth(property_name, station)
        return stats.pearsonr(cut_obs_arr[:,1], interp_model_arr[:,1])[0]




class CampaignPlotter(Campaign):

    def __init__(self, model_profiles_location, obs_profiles_location):
        super().__init__(model_profiles_location, obs_profiles_location)
    
    def add_property_to_subplot(self, ax, property_name, station, xlim=None, ylim=None, xlabel=None, ylabel=None, legend=False):
        model_prop = self.get_model_prop_arr(property_name, station)
        obs_CTD_prop = None
        obs_sonda_prop = None
        try:
            obs_CTD_prop = self.get_obs_CTD_prop_arr(property_name, station)
        except FileNotFoundError:
            print('CTD file not found, ignoring')
        try:
            obs_sonda_prop = self.get_obs_sonda_prop_arr(property_name, station)
        except FileNotFoundError:
            print('sonda file not found, ignoring')
        
        ax.plot(model_prop[:,1], list(map(lambda x: -x, model_prop[:,0])), label='model')
        ax.scatter(model_prop[:,1], list(map(lambda x: -x, model_prop[:,0])))

        if obs_CTD_prop is not None:
            ax.plot(obs_CTD_prop[:,1], list(map(lambda x: -x, obs_CTD_prop[:,0])), label='CTD')
            ax.scatter(obs_CTD_prop[:,1], list(map(lambda x: -x, obs_CTD_prop[:,0])))
        
        if obs_sonda_prop is not None:
            ax.plot(obs_sonda_prop[:,1], list(map(lambda x: -x, obs_sonda_prop[:,0])), label='sonda')
            ax.scatter(obs_sonda_prop[:,1], list(map(lambda x: -x, obs_sonda_prop[:,0])))
        
        ax.set_title(station)

        if ylim: ax.set_ylim(ylim[0], ylim[1])
        if xlim: ax.set_xlim(xlim[0], xlim[1])
        
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)
        
        ax.invert_yaxis()

        if legend: ax.legend()
    

    def add_property_error_to_subplot(self, ax, property_name, station, xlabel=None, ylabel=None, legend=False):
        model_prop = self.get_model_prop_arr(property_name, station)
        obs_prop = self.get_best_obs_prop_arr(property_name, station)
        
        obs_prop, interp_model_prop = interpolate_model_to_obs_depths(model_prop, obs_prop)
        
        ax.plot(obs_prop[:,1] - interp_model_prop[:,1], list(map(lambda x: -x,  obs_prop[:,0])), label='error')
        ax.scatter(obs_prop[:,1] - interp_model_prop[:,1], list(map(lambda x: -x, obs_prop[:,0])))
        
        ax.set_title(station)
        
        ax.invert_yaxis()

        if legend: ax.legend()
        

    def plot_property(self, property_name, x_limits=None):
        print(property_name)
        print(self.stations)
        mlp.rcParams['lines.linewidth'] = 1
        mlp.rcParams['lines.markersize'] = 3
        mlp.rcParams['font.size'] = 8

        if x_limits:
            xlim_min = x_limits[0]
        else:
            xlim_min = min([min(self.get_model_prop_arr(property_name, s)[:,1]) for s in self.stations])
            try: xlim_min = min(xlim_min, min([min(self.get_obs_CTD_prop_arr(property_name, s)[:,1]) for s in self.stations]))
            except FileNotFoundError: pass
            try: xlim_min = min(xlim_min, min([min(self.get_obs_sonda_prop_arr(property_name, s)[:,1]) for s in self.stations]))
            except FileNotFoundError: pass
        
        if x_limits:
            xlim_max = x_limits[1]
        else:
            xlim_max = max([max(self.get_model_prop_arr(property_name, s)[:,1]) for s in self.stations])
            try: xlim_max = max(xlim_max, max([max(self.get_obs_CTD_prop_arr(property_name, s)[:,1]) for s in self.stations]))
            except FileNotFoundError: pass
            try: xlim_max = max(xlim_max, max([max(self.get_obs_sonda_prop_arr(property_name, s)[:,1]) for s in self.stations]))
            except FileNotFoundError: pass
        
        xlim_margin = 0.05
        xlim = [xlim_min - xlim_margin*(xlim_max - xlim_min), xlim_max + xlim_margin*(xlim_max - xlim_min)]
        ylim = [0, 25]

        xlabel = property_name
        ylabel = 'Depth $(m)$'

        if len(self.stations) <= 2:
            fig, axes = plt.subplots(1, 2)
            fig.set_size_inches(6.3, 3.3)
            axes_loc = [axes[0], axes[1]]
        elif 2 < len(self.stations) <= 4:
            fig, axes = plt.subplots(2, 2)
            fig.set_size_inches(6.3, 6.3)
            axes_loc =[axes[0,0], axes[0,1], axes[1,0], axes[1,1]]
        
        fig.subplots_adjust(wspace=0.25, hspace=0.3)

        for n in range(0, len(self.stations)):
            legend = True if n == 0 else False
            self.add_property_to_subplot(axes_loc[n], property_name, self.stations[n], xlim=xlim, ylim=ylim, xlabel=xlabel, ylabel=ylabel, legend=legend)

        fig.suptitle(self.date_to_cp_number(datetime.strftime(self.date, '%Y-%m-%d'))+'\n'+datetime.strftime(self.date, '%Y-%m-%d')+'\n'+property_name)

        figname = './comparison/' + property_name + '.pdf'
        fig.savefig(figname)
        plt.close(fig=fig)


    def plot_property_error(self, property_name):

        mlp.rcParams['lines.linewidth'] = 1
        mlp.rcParams['lines.markersize'] = 3
        mlp.rcParams['font.size'] = 8

        xlabel = property_name
        ylabel = 'Depth $(m)$'

        if len(self.stations) <= 2:
            fig, axes = plt.subplots(1, 2)
            fig.set_size_inches(6.3, 3.3)
            axes_loc = [axes[0], axes[1]]
        elif 2 < len(self.stations) <= 4:
            fig, axes = plt.subplots(2, 2)
            fig.set_size_inches(6.3, 6.3)
            axes_loc =[axes[0,0], axes[0,1], axes[1,0], axes[1,1]]
        
        fig.subplots_adjust(wspace=0.25, hspace=0.3)

        for n in range(0, len(self.stations)):
            legend = True if n == 0 else False
            self.add_property_error_to_subplot(axes_loc[n], property_name, self.stations[n], xlabel=xlabel, ylabel=ylabel, legend=legend)

        fig.suptitle(datetime.strftime(self.date, '%Y-%m-%d')+'\n'+property_name)

        figname = './comparison/error_' + property_name + '.pdf'
        fig.savefig(figname)
        plt.close(fig=fig)
    
    def date_to_cp_number(self, date):
        cp_dates = {'2018-06-29': 'campanha 1',
                    '2018-10-25': 'campanha 2',
                    '2019-03-12': 'campanha 3',
                    '2019-04-30': 'campanha 4',
                    '2019-05-23': 'campanha 5'
                    }
        return cp_dates[date]
###############################################################################