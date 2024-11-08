# File for quick testing and sanity checks

import pandas as pd
import os 
import re
from collections import defaultdict

csvPath = './NACC_data/sorted_preprocessed_cohorts/0csv/alzd.csv'
cohortPath = './NACC_data/sorted_preprocessed_cohorts/ALZD/'


fspgr_folders = defaultdict(list)
mprage_folders = defaultdict(list)
# reading the .csv file
df = pd.read_csv(csvPath)
# separating based on sequencing
df_fspgr = df[df['FSPGR'] == 1]
df_mprage = df[df['MPRAGE'] == 1]