#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:20:00 2020

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

import pdb

# Custom:
import sys
sys.path.append('../../')
sys.path.append('../utils/')
import plt_utils
import CrIS_utils

# =============================================================================
# Main
# =============================================================================
print('************************************************')
print('*                                              *')
print('*  Starting: plt_simple_aircraft_over_CrIS.py  *')
print('*                                              *')
print('************************************************')
print()

# User input outpath & suffix:
# ============================
plt_outfile_path = input('Please enter plot output path: ')
plt_suffix       = input('Please enter plot suffix (e.g., jpg, png): ')

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

level  = ''
level2 = ''
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

# User input CrIS scaling:
# ========================
cris_scaling = input('\nPlease enter CrIS scaling factor (ppmv -> ppbv: 1000); <ENTER> = none: ')
if ~(cris_scaling == ''):
    cris_scaling = np.float(cris_scaling)
    cris_value   = cris_value * cris_scaling

# User input lat/lon:
# ===================
lat_min = np.int_(input('\nPlease enter minimum latitude: '))
lat_max = np.int_(input('Please enter maximum latitude: '))
lon_min = np.int_(input('Please enter minimum longitude: '))
lon_max = np.int_(input('Please enter maximum longitude: '))

lat_range = [lat_min, lat_max]
lon_range = [lon_min, lon_max]

# User input vmin/vmax:
# ===================
vmin = np.float_(input('\nPlease enter minimum value: '))
vmax = np.float_(input('Please enter maximum value: '))

# User input point sum aircraft:
# ==============================
point_sum = np.int_(input('\nHow many aircraft points would you like to average (e.g., 100; 1 = no averaging): '))

# User input CrIS steps (degrees):
# ================================
cris_steps_lat = np.float_(input('\nPlease enter CrIS lat step size (degrees, e.g., 0.3): '))
cris_steps_lon = np.float_(input('Please enter CrIS lon step size (degrees, e.g., 0.4): '))

# Generate average aircraft field:
# ================================
hn3_aircraft_filtered = aircraft_data_filtered['NH3_ppbv']
lat_aircraft_filtered = aircraft_data_filtered['Latitude_deg']
lon_aircraft_filtered = aircraft_data_filtered['Longitude_deg']

aircraft_data_filtered_xmean_values = [np.mean(hn3_aircraft_filtered[i*point_sum:i*point_sum+point_sum-1]) for i in range(np.int_(np.floor(len(hn3_aircraft_filtered)/point_sum)))]
aircraft_data_filtered_xmean_lats   = [np.mean(lat_aircraft_filtered[i*point_sum:i*point_sum+point_sum-1]) for i in range(np.int_(np.floor(len(lat_aircraft_filtered)/point_sum)))]
aircraft_data_filtered_xmean_lons   = [np.mean(lon_aircraft_filtered[i*point_sum:i*point_sum+point_sum-1]) for i in range(np.int_(np.floor(len(lon_aircraft_filtered)/point_sum)))]

aircraft_data_filtered_xmean = pd.DataFrame({'Latitude_deg':aircraft_data_filtered_xmean_lats,
                                             'Longitude_deg':aircraft_data_filtered_xmean_lons,
                                             'NH3_ppbv':aircraft_data_filtered_xmean_values})
aircraft_data_filtered_xmean

# Generate pixelized CrIS field:
# ==============================
print()
cris_pixel_field = CrIS_utils.CRIS_TO_PIXEL(cris_value,
                                            cris_lat,
                                            cris_lon,
                                            cris_steps_lat,
                                            cris_steps_lon,
                                            lat_range=lat_range,
                                            lon_range=lon_range)

# Plot:
# =====
lat_1 = lat_range[0]
lat_2 = lat_range[1]
lon_1 = lon_range[0]
lon_2 = lon_range[1]

pixel_lons = cris_pixel_field.columns
pixel_lats = cris_pixel_field.index

fig, ax = plt.subplots(figsize=(8,8),dpi=300)

ax.pcolormesh(pixel_lons,pixel_lats,cris_pixel_field.values,
              cmap='RdYlGn_r',
              vmin=vmin,
              vmax=vmax,
              shading='nearest')

# aircraft_data_filtered_15mean
aircraft_data_filtered_xmean.plot(kind='scatter',
                                  x='Longitude_deg',
                                  y='Latitude_deg',
                                  c='NH3_ppbv',
                                  cmap='RdYlGn_r',
                                  vmin=vmin,
                                  vmax=vmax,
                                  s=25,
                                  edgecolor='black',
                                  lw=0.2,
                                  ax=ax,
                                  marker="o",
                                  title=r'HN$_{3}$ (ppbv)',
                                  zorder=4)

if (level != '') & (level2 != ''):
    plt_outfile_name = f'{plt_outfile_path}/aircraft_{point_sum}_over_CrIS_{key}_l1-{level}_l2-{level2}_{cris_steps_lat}latx{cris_steps_lon}lon_simple.{plt_suffix}'

elif (level != ''):
    plt_outfile_name = f'{plt_outfile_path}/aircraft_{point_sum}_over_CrIS_{key}_l1-{level}_{cris_steps_lat}latx{cris_steps_lon}lon_simple.{plt_suffix}'

else:
    plt_outfile_name = f'{plt_outfile_path}/aircraft_{point_sum}_over_CrIS_{key}_{cris_steps_lat}latx{cris_steps_lon}lon_simple.{plt_suffix}'

print(f'\nPlotting:\n{plt_outfile_name}\n')
fig.savefig(plt_outfile_name,transparent=False,bbox_inches='tight')

plt.close(fig)

print('\nDONE!\n')
