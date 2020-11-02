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
from datetime import datetime
import pylab
import glob
import netCDF4

import pdb

# =============================================================================
# Hard-wired
# =============================================================================
plt_save_path = '../../../../plt/Ammonia/AKs'

# =============================================================================
# Main
# =============================================================================
print('***************************************')
print('*                                     *')
print('*  Starting: plt_example_file_aks.py  *')
print('*                                     *')
print('***************************************')
print()

# Find example file:
# ==================
CrIS_infile = glob.glob(f"../../../../Data/Ammonia/CrIS/*withWinds.nc")[0]

# Load example CrIS data:
# =======================
CrIS_data = netCDF4.Dataset(CrIS_infile)

# Cycle through AKs and plot:
# ===========================
for n_ak in range(len(CrIS_data['avg_kernel'][:,0,0])):
    this_pressure = CrIS_data['pressure'][n_ak,:]

    # Ensure pressure range is valid:
    start_index = 0
    while this_pressure[0] < -999.:
        start_index += 1
        this_pressure = CrIS_data['pressure'][n_ak,start_index:]

    this_profile  = CrIS_data['xretv'][n_ak,start_index:]*1000
    this_AK       = CrIS_data['avg_kernel'][n_ak,start_index:,start_index:]
    this_qflag    = '{:d}'.format(np.int_(CrIS_data['Quality_Flag'][n_ak]))
    this_DOF      = '{:<5.3f}'.format(np.float_(CrIS_data['DOF'][n_ak]))
    this_chi2     = '{:<5.3f}'.format(np.float_(CrIS_data['CHISQ'][n_ak]))
    lat = '{:<6.2f}'.format(CrIS_data['Latitude'][n_ak])
    lon = '{:<6.2f}'.format(CrIS_data['Longitude'][n_ak])

    this_AK_df = pd.DataFrame(this_AK,index=this_pressure,columns=this_pressure)

    # Plot:
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12,8), dpi=150,
                                   sharey=True, gridspec_kw={'width_ratios': [2, 1]})

    for i in this_AK_df.index:
        ax1.plot(this_AK_df[i].values,
                 this_AK_df.columns,
                 marker='o',
                 label=i)
    ax1.set_ylim(1000,0)
    ax1.legend()
    ax1.set_title(f"CrIS AK {n_ak}: "+lat+r"$\degree$"+"N "+lon+r"$\degree$ E"+
                  f'\nqflag = {this_qflag}; DOF = {this_DOF}; '+r'$\chi^2$'+f' = {this_chi2}')
    ax1.set_ylabel('pressure (hPa)')

    ax2.plot(this_profile,
             this_pressure,
             color='black')
    # ax2.set_ylim(1000,0)
    ax2.set_title(r'NH$_3$')
    ax2.set_xlabel('vmr (ppbv)')

    # Save:
    n_ak_string   = '{:04d}'.format(n_ak)
    plt_save_file = f'{plt_save_path}/All_AKs_example_file_AK_{n_ak_string}.jpg'
    print(f'\nPlotting:\n{plt_save_file}')
    fig.savefig(plt_save_file,transparent=False,bbox_inches='tight')

    plt.close(fig)

print('\nDONE!\n')
