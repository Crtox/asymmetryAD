# File for quick testing and sanity checks

import pandas as pd
import os 

dataPath = "./NACC_data/sorted_cohorts/"
# dataPath = os.path.abspath(dataPath)

# if os.name ==  'nt':
#     dataPath = '\\\\?\\' + dataPath

df_nc = pd.read_csv(dataPath  + 'nc.csv')
df_mci = pd.read_csv(dataPath + 'mci.csv')
df_alz = pd.read_csv(dataPath + 'alzd.csv')
df_trans = pd.read_csv(dataPath + 'trans.csv')

nc_filenames = list(df_nc['NACCMRFI'])
mci_filenames = list(df_mci['NACCMRFI'])
alz_filenames = list(df_alz['NACCMRFI'])
trans_filenames = list(df_trans['NACCMRFI'])

nc_dir_filenames = os.listdir(dataPath + 'NC')
mci_dir_filenames = os.listdir(dataPath + 'MCI')
alzd_dir_filenames = os.listdir(dataPath + 'ALZD')
trans_dir_filenames = os.listdir(dataPath + 'TRANS')

print(nc_dir_filenames)