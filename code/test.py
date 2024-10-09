# File for quick testing and sanity checks

import pandas as pd
import os 
import re

alzdPath = './NACC_data/sorted_cohorts/ALZD/'
alzdPath = os.path.abspath(alzdPath)

if os.name == 'nt':                     
    alzdPath = '\\\\?\\' + alzdPath

nacc_pattern = 'NACC'



for folder in os.listdir(alzdPath): 

    folder_path = os.path.join(alzdPath, folder)

    if re.match(nacc_pattern, folder):
            
        # these type can have both MPRAGE or FSPGR 
        subfolder_fp = os.path.join(folder_path, os.listdir(folder_path)[0])

        sub_subfolder_fp = os.path.join(subfolder_fp, os.listdir(subfolder_fp)[0])

        sub_sub_subfolder = os.path.join(sub_subfolder_fp, os.listdir(sub_subfolder_fp)[0])

        for f in sub_sub_subfolder: 

            if f.endswith('.json'):

                print(f)