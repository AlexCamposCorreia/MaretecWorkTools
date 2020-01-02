import numpy as np
from scipy.interpolate import interp1d
from common_functions.get_data import get_data


def interpolate_model_to_obs_depths(model_arr, obs_arr):
    obs_arr = np.array([x for x in obs_arr if model_arr[-1,0] < x[0] < model_arr[0,0]])
    f = interp1d(model_arr[:,0], model_arr[:,1])
    return obs_arr, np.column_stack((obs_arr[:,0], f(obs_arr[:,0])))
