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
#             Function to separate FSPGR and MPRAGE sequencings and store their folders' paths                 #
#--------------------------------------------------------------------------------------------------------------#

def separate_sequencing(cohort_path, csv_path):
    # empty dictionaries to store NACCID as key and NACCMRFI as values
    fspgr_folders = defaultdict(list)
    mprage_folders = defaultdict(list)
    # reading the .csv file
    df = pd.read_csv(csv_path)
    # separating based on sequencing
    df_fspgr = df[df['FSPGR'] == 1]
    df_mprage = df[df['MPRAGE'] == 1]
    # iterating throught each patient
    for naccid in df_fspgr['NACCID'].unique():
        # extracting the patients data
        patient_data = df_fspgr[df_fspgr['NACCID'] == naccid]
        # getting all the file names under that patient
        folder_names = [os.path.join(cohort_path, row['NACCMRFI']) for idx, row in patient_data.iterrows()]
        # appending the file names to value of NACCID as key
        fspgr_folders[naccid] = folder_names
    # same for mprage
    for naccid in df_mprage['NACCID'].unique():
        patient_data = df_mprage[df_mprage['NACCID'] == naccid]
        folder_names = [os.path.join(cohort_path, row['NACCMRFI']) for idx, row in patient_data.iterrows()]
        mprage_folders[naccid] = folder_names
    # returning the dictionaries
    return fspgr_folders, mprage_folders



#--------------------------------------------------------------------------------------------------------------#
#                      Function to store .nii files, fspgr and mprage separately                               #
#--------------------------------------------------------------------------------------------------------------#

# storing NACCID as key and filepaths to .nii files as values
def filepaths(cohort_path, csv_path):
    # empty dictionaries to store .nii filepaths
    wbet_fspgr_files = defaultdict(list)
    wbet_mprage_files = defaultdict(list)
    # wbet pattern
    pattern = 'wbet'
    # loading dictionaries storing paths to parent folders
    fspgr_folders = separate_sequencing(cohort_path, csv_path)[0]
    mprage_folders = separate_sequencing(cohort_path, csv_path)[1]
    # iterating and accesing the files inside the folders
    for naccid, folder_paths in fspgr_folders.items():
        for folder in folder_paths:
            files = os.listdir(folder)
            for file in files:
                file_path = os.path.join(folder, file)
                if pattern in file:
                    wbet_fspgr_files[naccid].append(file_path)
    # same for mprage
    for naccid, folder_paths in mprage_folders.items():
        for folder in folder_paths:
            files = os.listdir(folder)
            for file in files:
                file_path = os.path.join(folder, file)
                if pattern in file:
                    wbet_mprage_files[naccid].append(file_path)
    return wbet_fspgr_files, wbet_mprage_files



#--------------------------------------------------------------------------------------------------------------#
#                   Function to store NACCID as keys and time from first scan as values                        #
#--------------------------------------------------------------------------------------------------------------#

def time_from_baseline(csv_path):
    # empty dictionary
    patient_scan_dates = defaultdict(list)
    # reading .csv file
    df = pd.read_csv(csv_path)
    for naccid in df['NACCID'].unique():
        # extracting the patients data
        patient_data = df[df['NACCID'] == naccid]
        # extracting days, months and years of scan
        months = [row['MRIMO'] for idx, row in patient_data.iterrows()]
        days = [row['MRIDY'] for idx, row in patient_data.iterrows()]
        years = [row['MRIYR'] for idx, row in patient_data.iterrows()]
        # array to store dates
        dates = np.zeros(len(months), dtype=object)
        for i in range(len(months)):
            dates[i] = ('{}-{}-{}'.format(years[i], months[i], days[i]))
            dates[i] = parser.parse(dates[i])
        # calculating time differences between scans
        diffs = [(dates[i] - dates[0]) for i in dates]
        # adding to array
        patient_scan_dates[naccid].append(diffs)
    return patient_scan_dates