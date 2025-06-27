# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 15:33:15 2025

@author: aydina

Script to calculate priority scores for sampled 266 businesses
"""

import pandas as pd
import numpy as np

path_to_universe_file = '...../universeConsolidated_267_202506.csv'

# Read universe file
universe = pd.read_csv(path_to_universe_file)

# %% Prepare data
# Calculate the size of each cell in the universe
cell_size_universe = universe['cell_no'].value_counts().sort_index()
cell_size_universe.name = 'universe'

# Filter non-seleceted businesses
selection = universe[universe['selmkr'] != 'N'][['ruref','frosic2007','cell_no',
                                                 'selmkr','frotover']]

# Calculate the size of each cell in the sample
cell_size_sample = selection['cell_no'].value_counts().sort_index()
cell_size_sample.name = 'sample'

# Merge cell_size series
cell_df = pd.concat([cell_size_sample, cell_size_universe], axis=1)

# Calculate the design weight
cell_df['weight'] = cell_df['universe']/cell_df['sample']

df = pd.merge(selection, cell_df, left_on='cell_no', right_index=True)

# %% Calculate the priority score 
# Baseline
df['base_score'] = df['weight']*df['frotover']

# For holding companies, set them missing
df.loc[df['frosic2007'] < 64300, 'base_score'] = np.nan

#Rank-Based Normalization (Percentile Ranking) by SIC
df['normalised_score'] = df.groupby('frosic2007')['base_score'].rank(pct=True)

# Set max scores for reference list
df.loc[df['selmkr']=='L', 'normalised_score'] = 0.99

df = df.sort_values(['frosic2007','normalised_score'])