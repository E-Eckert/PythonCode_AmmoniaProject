#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:00:00 2020

@author: elleneckert
"""
# =============================================================================
# Import:
# =============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#==============================================================================
#   CRIS_PIXEL_PLOT
#==============================================================================
def CRIS_PIXEL_PLOT(data2plot,
                    lat,
                    lon,
                    stepsize_lat,
                    stepsize_lon,
                    ax,
                    vmin=0,
                    vmax=0,
                    lat_range=[np.nan,np.nan],
                    lon_range=[np.nan,np.nan]):
    '''
    Plots binned mean CrIS data of data2plot using Seaborn.
    INPUT:
        - data2plot: 1d array of same length as lat & lon
                     --> CrIS_data['tot_col'][:]
        - lat: latitude array  --> CrIS_data['Latitude'][:]
        - lon: longitude array --> CrIS_data['Longitude'][:]
        - stepsize_lat: in degrees
        - stepsize_lon: in degrees
        - vmin: minimun data value
        - vmax: maximum data value
        - lat_range / lon_range = [lat_min,lat_max] / [lon_min,lon_max]
                    --> default [np.nan,np.nan] --> entire field is plotted

    OUTPUT:
        - ax: ax of figure     --> fig, ax = plt.subplots(figsize=(8,8),dpi=300)
    '''
    print('*******************************')
    print('*                             *')
    print('*  Starting: CRIS_PIXEL_PLOT  *')
    print('*                             *')
    print('*******************************')
    print()

    cris_help_df = pd.DataFrame({'lat':np.array(lat),
                                 'lon':np.array(lon),
                                 'value':np.array(data2plot)})

    cris_min = np.floor(cris_help_df.min())
    cris_max = np.ceil(cris_help_df.max())

    # Latitudes:
    # ==========
    lat_num = np.int_((cris_max['lat']-cris_min['lat'])*1/stepsize_lat+1)
    lat_num

    lat_steps = np.linspace(cris_min['lat'], cris_max['lat'], num=lat_num, endpoint=True)
    lat_steps = lat_steps[::-1]
    lat_steps

    lat_grid = np.round([np.mean((lat_steps[i],lat_steps[i+1]))*100 for i in range(len(lat_steps)-1)])/100
    lat_grid

    # Longitudes:
    # ===========
    lon_num = np.int_((cris_max['lon']-cris_min['lon'])*1/stepsize_lon+1)
    lon_num

    lon_steps = np.linspace(cris_min['lon'], cris_max['lon'], num=lon_num, endpoint=True)
    lon_steps

    lon_grid = np.round([np.mean((lon_steps[i],lon_steps[i+1]))*100 for i in range(len(lon_steps)-1)])/100
    lon_grid

    # Create Pandas DataFrame:
    # ========================
    CrIS_binned_totcol    = np.zeros((len(lat_grid),len(lon_grid)))
    CrIS_binned_totcol[:] = np.nan

    CrIS_binned_df = pd.DataFrame(CrIS_binned_totcol,index=lat_grid,columns=lon_grid)

    # Fill entries:
    lat_plus_minus = (lat_grid[1]-lat_grid[0])/2.
    lon_plus_minus = (lon_grid[1]-lon_grid[0])/2.

    for lat in lat_grid:
        for lon in lon_grid:
            index = np.where((cris_help_df['lat'] < (lat-lat_plus_minus)) &
                             (cris_help_df['lat'] > (lat+lat_plus_minus)) &
                             (cris_help_df['lon'] > (lon-lon_plus_minus)) &
                             (cris_help_df['lon'] < (lon+lon_plus_minus)))
            bin_mean = (cris_help_df.iloc[index])['value'].mean()
            CrIS_binned_df.loc[lat,lon] = bin_mean

    if np.isfinite(lat_range).all():
        lat_subindex = np.where((CrIS_binned_df.index < lat_range[1]) & (CrIS_binned_df.index > lat_range[0]))
        sub_array = CrIS_binned_df.iloc[lat_subindex]
    else:
        sub_array = CrIS_binned_df

    if np.isfinite(lon_range).all():
        lon_subindex = np.where((CrIS_binned_df.columns < lon_range[1]) & (CrIS_binned_df.columns > lon_range[0]))
        sub_array = sub_array[CrIS_binned_df.columns[lon_subindex]]

    sns.heatmap(sub_array,
                ax=ax,
                cmap='RdYlGn_r',
                vmin=vmin,
                vmax=vmax)


    return True

#==============================================================================
#   CRIS_TO_GEOPANDAS_PIXEL
#==============================================================================
def CRIS_TO_PIXEL(data2plot,
                  lat,
                  lon,
                  stepsize_lat,
                  stepsize_lon,
                  lat_range=[np.nan,np.nan],
                  lon_range=[np.nan,np.nan]):
    '''
    Creates a binned Pandas DataFrame of CrIS data.
    INPUT:
        - data2plot: 1d array of same length as lat & lon
                     --> CrIS_data['tot_col'][:]
        - lat: latitude array  --> CrIS_data['Latitude'][:]
        - lon: longitude array --> CrIS_data['Longitude'][:]
        - stepsize_lat: in degrees
        - stepsize_lon: in degrees
        - vmin: minimun data value
        - vmax: maximum data value
        - lat_range / lon_range = [lat_min,lat_max] / [lon_min,lon_max]
                    --> default [np.nan,np.nan] --> entire field is plotted

    OUTPUT:
        - ax: ax of figure     --> fig, ax = plt.subplots(figsize=(8,8),dpi=300)
    '''
    print('*****************************')
    print('*                           *')
    print('*  Starting: CRIS_TO_PIXEL  *')
    print('*                           *')
    print('*****************************')
    print()

    cris_help_df = pd.DataFrame({'lat':np.array(lat),
                                 'lon':np.array(lon),
                                 'value':np.array(data2plot)})

    cris_min = np.floor(cris_help_df.min())
    cris_max = np.ceil(cris_help_df.max())

    # Latitudes:
    # ==========
    lat_num = np.int_((cris_max['lat']-cris_min['lat'])*1/stepsize_lat+1)

    lat_steps = np.linspace(cris_min['lat'], cris_max['lat'], num=lat_num, endpoint=True)
    lat_steps = lat_steps[::-1]

    lat_grid = np.round([np.mean((lat_steps[i],lat_steps[i+1]))*100 for i in range(len(lat_steps)-1)])/100

    # Longitudes:
    # ===========
    lon_num = np.int_((cris_max['lon']-cris_min['lon'])*1/stepsize_lon+1)
    lon_steps = np.linspace(cris_min['lon'], cris_max['lon'], num=lon_num, endpoint=True)

    lon_grid = np.round([np.mean((lon_steps[i],lon_steps[i+1]))*100 for i in range(len(lon_steps)-1)])/100

    # Create Pandas DataFrame:
    # ========================
    CrIS_binned_values    = np.zeros((len(lat_grid),len(lon_grid)))
    CrIS_binned_values[:] = np.nan

    CrIS_binned_df = pd.DataFrame(CrIS_binned_values,index=lat_grid,columns=lon_grid)

    # Fill entries:
    lat_plus_minus = (lat_grid[1]-lat_grid[0])/2.
    lon_plus_minus = (lon_grid[1]-lon_grid[0])/2.

    for lat in lat_grid:
        for lon in lon_grid:
            index = np.where((cris_help_df['lat'] < (lat-lat_plus_minus)) &
                             (cris_help_df['lat'] > (lat+lat_plus_minus)) &
                             (cris_help_df['lon'] > (lon-lon_plus_minus)) &
                             (cris_help_df['lon'] < (lon+lon_plus_minus)))
            bin_mean = (cris_help_df.iloc[index])['value'].mean()
            CrIS_binned_df.loc[lat,lon] = bin_mean

    if np.isfinite(lat_range).all():
        lat_subindex = np.where((CrIS_binned_df.index < lat_range[1]) & (CrIS_binned_df.index > lat_range[0]))
        sub_array = CrIS_binned_df.iloc[lat_subindex]
    else:
        sub_array = CrIS_binned_df

    if np.isfinite(lon_range).all():
        lon_subindex = np.where((CrIS_binned_df.columns < lon_range[1]) & (CrIS_binned_df.columns > lon_range[0]))
        sub_array = sub_array[CrIS_binned_df.columns[lon_subindex]]

    return sub_array
