#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:20:00 2020

@author: elleneckert
"""
# =============================================================================
# Import:
# =============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab
import glob
import netCDF4
import seaborn as sns

import pdb

import os

# Custom:
import sys
sys.path.append('../../')
sys.path.append('../utils/')
import plt_utils
import CrIS_utils

# =============================================================================
# Main
# =============================================================================
print('*****************************************')
print('*                                       *')
print('*  Starting: plt_aircraft_over_CrIS.py  *')
print('*                                       *')
print('*****************************************')
print()

# Load Data:
# ==========
# Aircraft:
aircraft_infile = glob.glob(f"../../../../Data/Ammonia/Aircraft_Campaign_2018/*.csv")[0]
print(f'Reading aircraft file: \n{aircraft_infile}\n')
aircraft_data  = pd.read_csv(aircraft_infile)

# CrIS:
CrIS_infile = glob.glob(f"../../../../Data/Ammonia/CrIS/*.nc")[0]
print(f'Reading CrIS file: \n{CrIS_infile}\n')
CrIS_data   = netCDF4.Dataset(CrIS_infile)

# Filter Aircraft Data:
# =====================
aircraft_data[aircraft_data == -999.] = np.nan
aircraft_data_filtered = aircraft_data[aircraft_data['NH3_ppbv_flag'] == 'V0']

# CrIS processing:
# ================
CrIS_keys = list(CrIS_data.variables)
print(f'CrIS data fields:')
[print(i) for i in CrIS_keys]

cris_lat   = np.array(CrIS_data['Latitude'][:])
cris_lon   = np.array(CrIS_data['Longitude'][:])

key = input("\n> Please select field to plot: ")
cris_value = np.array(CrIS_data[key][:])

if cris_value.ndim == 2:
    n_levels   = np.shape(cris_value)[1]
    level      = np.int_(input(f'\n> {key} has {n_levels} levels. Please select level to plot (0-{n_levels-1}): '))

    cris_value = cris_value[:,level]

if cris_value.ndim == 3:
    n_levels  = np.shape(cris_value)[1]
    n_levels2 = np.shape(cris_value)[2]
    print(f'\n> {key} has {n_levels} levels.')
    level     = np.int_(input(f'> Please select level 1 to plot (0-{n_levels-1}): '))
    level2    = np.int_(input(f'> Please select level 2 to plot (0-{n_levels2-1}): '))

    cris_value = cris_value[:,level,level2]

# User input lat/lon:
# ===================

lat_min = np.int_(input('\nPlease enter minimum latitude: '))
lat_max = np.int_(input('Please enter maximum latitude: '))
lon_min = np.int_(input('Please enter minimum longitude: '))
lon_max = np.int_(input('Please enter maximum longitude: '))

lat_range = [lat_min, lat_max]
lon_range = [lon_min, lon_max]

# shapefile_path = input('\nPlease enter Cartopy shape file path (default: /mnt/d/GoogleDrive/Python/Shape_Files): \n')
#
# if shapefile_path == '':
#     fig, ax, crs, crs_proj4 = plt_utils.PLT_MAP_GEOPANDAS(lat_range, lon_range)
# else:
#     fig, ax, crs, crs_proj4 = plt_utils.PLT_MAP_GEOPANDAS(lat_range, lon_range, shapefile_path)
#
cris_pixel_field = CrIS_utils.CRIS_TO_GEOPANDAS_PIXEL(cris_value,
                                   cris_lat,
                                   cris_lon,
                                   0.3,
                                   0.4,
                                   lat_range=lat_range,
                                   lon_range=lon_range)

# TEST PART:
# ==========
center_point   = [np.mean(lat_range), np.mean(lon_range)]

map_locations  = pd.DataFrame({'lat':[center_point[0]],
                               'lon':[center_point[1]]})

lat_0 = map_locations['lat']
lon_0 = map_locations['lon']
lat_1 = lat_range[0]
lat_2 = lat_range[1]
lon_1 = lon_range[0]
lon_2 = lon_range[1]

import cartopy.crs as ccrs
crs = ccrs.LambertConformal(central_longitude=center_point[1],
                            central_latitude=center_point[0],
                            false_easting=0.0,
                            false_northing=0.0,
                            secant_latitudes=None,
                            standard_parallels=None,
                            globe=None)

fig, ax = plt.subplots(figsize=(12,9), dpi=600, subplot_kw={'projection': crs})

pixel_lons = cris_pixel_field.columns
pixel_lats = cris_pixel_field.index
x,y=np.meshgrid(pixel_lons,pixel_lats)
# transform = crs # ._as_mpl_transform(ax)
ax.pcolormesh(x,y,cris_pixel_field.values,
              vmin=0,
              vmax=1e17,
              cmap='RdYlGn_r',
              transform=ccrs.PlateCarree()) #,ax=ax) #,latlon=True)
#
# cris_pixel_field.plot(ax=ax, transform=transform)

import cartopy.feature as cf
ax.add_feature(cf.NaturalEarthFeature(
               category='cultural',
               name='admin_0_countries',
               scale='50m',
               facecolor='none'))
ax.add_feature(cf.NaturalEarthFeature(
               category='cultural',
               name='admin_1_states_provinces_lines',
               scale='50m',
               facecolor='none'))
ax.add_feature(cf.NaturalEarthFeature(
               category='physical',
               name='lakes',
               scale='50m',
               facecolor='none'))
ax.coastlines('50m')
ax.add_feature(cf.BORDERS)

fig.savefig('test.pdf',transparent=False,bbox_inches='tight')

plt.close(fig)

# pdb.set_trace()
