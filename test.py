import numpy as np 

data_npz = 'data/npz/all_data.npz'

time = np.load(data_npz)['time']


map_lon = np.load(data_npz)['map_lon']
map_lat = np.load(data_npz)['map_lat']
map_cloud_cover = np.load(data_npz)['map_cloud_cover']
map_sea_level = np.load(data_npz)['map_sea_level']
map_surface_temp = np.load(data_npz)['map_surface_temp']
map_wind_u_mean = np.load(data_npz)['map_wind_u_mean']
map_wind_v_mean = np.load(data_npz)['map_wind_v_mean']


print(map_surface_temp.shape)