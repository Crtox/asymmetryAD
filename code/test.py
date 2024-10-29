# File for quick testing and sanity checks

import pandas as pd
import os 
import re

alzdPath = './NACC_data/sorted_preprocessed_cohorts/0csv/alzd.csv'

df = pd.read_csv(alzdPath)
df_fspgr = df[df['FSPGR'] == 1]
df_mprage = df[df['MPRAGE'] == 1]
fspgr_files = [row['NACCMRFI'] for idx, row in df_fspgr.iterrows()]
mprage_files = [row['NACCMRFI'] for idx, row in df_mprage.iterrows()]
    
