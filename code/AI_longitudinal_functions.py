#--------------------------------------------------------------------------------------------------------------#
#                       Script to store functions used in "AI_longitudinal.ipynb"                              #
#                                                                                                              #
#                                      Črt Rozman, October 2024                                                #
#--------------------------------------------------------------------------------------------------------------#

import os 
import re
import pandas as pd
import numpy as np
from dateutil import parser
from collections import defaultdict
import nibabel as nib
import matplotlib.pyplot as plt



#--------------------------------------------------------------------------------------------------------------#
#                 Function to separate FSPGR and MPRAGE sequencings and store their file paths                 #
#--------------------------------------------------------------------------------------------------------------#

def separate_sequencing(folder_path, csv_path):
    # reading the .csv file containing info on sequencing types
    df = pd.read_csv(csv_path)
    # separating fspgr and mprage data format
    df_fspgr = df[df['FSPGR'] == 1]
    df_mprage = df[df['MPRAGE'] == 1]
    # reading the folder name and storing it into array
    fspgr_files = [row['NACCMRFI'] for idx, row in df_fspgr.iterrows()]
    mprage_files = [row['NACCMRFI'] for idx, row in df_mprage.iterrows()]
    # storing the full path instead of just folder names
    fspgr_files_paths = [os.path.join(folder_path, f) for f in fspgr_files]
    mprage_files_paths = [os.path.join(folder_path, f) for f in mprage_files]
    return fspgr_files_paths, mprage_files_paths



# only taking the wbet .nii files (whole brains)
def filepaths(folder_path, csv_path):
    wbet_fspgr_files_paths = []
    wbet_mprage_files_paths = []
    # patterns for our wbet files
    fspgr_pattern = re.compile(r'wbet_crf_rsl_([A-Z0-9]{6})')
    mprage_pattern = re.compile(r'wbet_crf_rsl_(S[0-9]{3})')
    # getting the folder files paths
    fspgr_files_paths = separate_sequencing(folder_path, csv_path)[0]
    mprage_files_paths = separate_sequencing(folder_path, csv_path)[1]
    # iterating inside folder
    for file in os.listdir(fspgr_files_paths):
        match = fspgr_pattern.search(file)
        if match:
            wbet_fspgr_files_paths.append(file)
    for file in os.listdir(mprage_files_paths):
        match = mprage_pattern.search(file)
        if match:
            wbet_mprage_files_paths.append(file)
    return wbet_fspgr_files_paths, wbet_mprage_files_paths