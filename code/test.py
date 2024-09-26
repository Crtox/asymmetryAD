# File for quick testing and sanity checks

import pandas as pd

loadPath = './python/data/'

df = pd.read_csv(loadPath + 'MRIT1_longitudinal_UDS_narrow_v2.csv')

unique_count = df['NACCID'].nunique()

print(unique_count)