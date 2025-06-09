# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 13:39:01 2025

@author: aydina

Script to calculate priority scores for sampled 266 businesses
"""

import pandas as pd
import numpy as np

path_to_universe_file = '...../universeConsolidated_400_202409.csv'

# Read universe file
universe = pd.read_csv(path_to_universe_file)

# Calculate the size of each cell in the universe
cell_size_universe = universe['cell_no'].value_counts().sort_index()
cell_size_universe.name = 'universe'

# Filter non-seleceted businesses
selection = universe[universe['selmkr'] != 'N'][['ruref','frosic2007','cell_no','selmkr','Total Assets']]

# Calculate the size of each cell in the sample
cell_size_sample = selection['cell_no'].value_counts().sort_index()
cell_size_sample.name = 'sample'

# Merge cell_size series
cell_df = pd.concat([cell_size_sample, cell_size_universe], axis=1)

# Calculate the design weight
cell_df['weight'] = cell_df['universe']/cell_df['sample']

df = pd.merge(selection, cell_df, left_on='cell_no', right_index=True)

####### Calculate the priority score #######
# Baseline
df['score'] = df['weight']*df['Total Assets']

# Logarithm of baseline score
df['log_score'] = np.log(df['score']+1)