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

def separate_sequencing_dictionary(cohort_path, csv_path):
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
def filepaths_dictionary(cohort_path, csv_path):
    # empty dictionaries to store .nii filepaths
    wbet_fspgr_files = defaultdict(list)
    wbet_mprage_files = defaultdict(list)
    # wbet pattern
    pattern = 'wbet'
    # loading dictionaries storing paths to parent folders
    fspgr_folders = separate_sequencing_dictionary(cohort_path, csv_path)[0]
    mprage_folders = separate_sequencing_dictionary(cohort_path, csv_path)[1]
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
        # array to store differences 
        diffs = []
        # array to store dates
        dates = np.zeros(len(months), dtype=object)
        for i in range(len(months)):
            dates[i] = ('{}-{}-{}'.format(years[i], months[i], days[i]))
            dates[i] = parser.parse(dates[i])
        for i in range(len(dates)):
            # substracting and dividing by average days in a year
            diffs.append((dates[i] - dates[0]).days / 365.25)
        # adding to array
        patient_scan_dates[naccid] = diffs
    return patient_scan_dates



#--------------------------------------------------------------------------------------------------------------#
#              Function to prepare patient data: load .nii files and flatten from 3D to 1D                     #
#--------------------------------------------------------------------------------------------------------------#

# takes in dictionary prepared by function "filepaths"
def flatten_and_normalize_across_all(nii_dictionary):
    # flatten all images and calculate the global sum
    flat_nii_files = defaultdict(list)
    total_sum = 0
    # flatten images and calculate the total sum
    for naccid, file_paths in nii_dictionary.items():
        for nii_file in file_paths:
            img = nib.load(nii_file)
            img_data = img.get_fdata()
            img_1d = img_data.flatten()
            flat_nii_files[naccid].append(img_1d)
            total_sum += np.sum(img_1d)
    # stack and normalize each NACCID’s images using the global sum
    normalized_flat_nii_files = {}
    for naccid, images_array in flat_nii_files.items():
        # stacking in columns
        stacked_images = np.column_stack(images_array)
        # normalizing
        normalized_images = stacked_images / total_sum
        normalized_flat_nii_files[naccid] = normalized_images
    return normalized_flat_nii_files


# the normalization part might be wrong, so again without normalization
def flatten(nii_dictionary):
    # flatten all images and calculate the global sum
    flat_nii_files = defaultdict(list)
    # flatten images and calculate the total sum
    for naccid, file_paths in nii_dictionary.items():
        for nii_file in file_paths:
            img = nib.load(nii_file)
            img_data = img.get_fdata()
            img_1d = img_data.flatten()
            flat_nii_files[naccid].append(img_1d)
    # stack and normalize each NACCID’s images using the global sum
    flat_nii_files_stacked = {}
    for naccid, images_array in flat_nii_files.items():
        # stacking in columns
        stacked_images = np.column_stack(images_array)
        # normalizing
        flat_nii_files_stacked[naccid] = stacked_images
    return flat_nii_files_stacked


#--------------------------------------------------------------------------------------------------------------#
#              Function to extract mask region names and function to get whole hemispheres as ROI              #
#--------------------------------------------------------------------------------------------------------------#

def mask_roi_titles(mask_txt_file):
    masks_title = []
    with open(mask_txt_file, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) > 1:
                masks_title.append(parts[1])
    masks_title_all = masks_title[:-1]               # all roi names
    masks_title_L = masks_title[:-1:2]               # left side roi names
    masks_title_R = masks_title[1::2]                # right side roi names
    return masks_title_all, masks_title_L, masks_title_R


def mask_hemispheres(mask_path, mask_txt_file, flatten=True):
    mask = nib.load(mask_path)                       # loading mask
    mask = mask.get_fdata()                          # extracting data
    # initializing empty arrays
    left_hemisphere_mask = np.zeros_like(mask, dtype=bool)         
    right_hemisphere_mask = np.zeros_like(mask, dtype=bool)       
    # iteration range is the lenght of masks_title_all (we iterate throught all rois)
    it_range = len(mask_roi_titles(mask_txt_file)[0]) + 1
    for i in range(1, it_range):
        # odd regions correspond to left hemisphere
        if i % 2 == 1:                         
            left_hemisphere_mask |= (mask == i)      # summing together all left regions
        # even regions correspond to right hemisphere
        else:
            right_hemisphere_mask |= (mask == i)     # summing together all right regions
    # flattening the arrays
    if flatten:
        left_hemisphere_mask = left_hemisphere_mask.flatten()   
        right_hemisphere_mask = right_hemisphere_mask.flatten()
    return left_hemisphere_mask, right_hemisphere_mask



#--------------------------------------------------------------------------------------------------------------#
#         Function to extracts different ROIs of mask (temporal, frontal lobe and hippocampus for now)         #
#--------------------------------------------------------------------------------------------------------------#

# ALERT: TERRIBLE CODE
def mask_regions(maskPath, flatten=True):
    # loading the mask
    mask = nib.load(maskPath + 'AAL3+pons.nii')
    mask = mask.get_fdata()
    # loading the masks titles
    masks_title_all = mask_roi_titles(maskPath + 'AAL3+pons.txt')[0]
    # ROI prefixes
    frontal_prefix = 'Frontal'
    temporal_prefix = 'Temporal'
    hippo_prefix = 'Hippocampus'
    # left and right prefixes
    L_prefix = 'L'
    R_prefix = 'R'
    # empty dictionaries to store roi names and indexes
    L_frontal_lobe = {}
    R_frontal_lobe = {}
    L_temporal_lobe = {}
    R_temporal_lobe = {}
    L_hippocampus = {}
    R_hippocampus = {}
    # iterating and adding to dictionaries
    for idx, title in enumerate(masks_title_all):
        if frontal_prefix in title and L_prefix in title:
            L_frontal_lobe[title] = idx
        if frontal_prefix in title and R_prefix in title:
            R_frontal_lobe[title] = idx
        elif temporal_prefix in title and L_prefix in title:
            L_temporal_lobe[title] = idx
        elif temporal_prefix in title and R_prefix in title:
            R_temporal_lobe[title] = idx
        elif hippo_prefix in title and L_prefix in title:
            L_hippocampus[title] = idx
        elif hippo_prefix in title and R_prefix in title:
            R_hippocampus[title] = idx
    # empty arrays, to be masks or ROI, same shape as mask
    mask_L_frontal_lobe = np.zeros_like(mask, dtype=bool)
    mask_R_frontal_lobe = np.zeros_like(mask, dtype=bool)
    mask_L_temporal_lobe = np.zeros_like(mask, dtype=bool)
    mask_R_temporal_lobe = np.zeros_like(mask, dtype=bool)
    mask_L_hippocampus = np.zeros_like(mask, dtype=bool)
    mask_R_hippocampus = np.zeros_like(mask, dtype=bool)
    # creating ROI masks
    for i in range(len(np.unique(mask))):
        for idx in L_frontal_lobe.values():
            if i == idx:
                mask_L_frontal_lobe |= (mask == i)
        for idx in R_frontal_lobe.values():
            if i == idx:
                mask_R_frontal_lobe |= (mask == i)
        for idx in L_temporal_lobe.values():
            if i == idx:
                mask_L_temporal_lobe |= (mask == i)
        for idx in R_temporal_lobe.values():
            if i == idx:
                mask_R_temporal_lobe |= (mask == i)
        for idx in L_hippocampus.values():
            if i == idx:
                mask_L_hippocampus |= (mask == i)
        for idx in R_hippocampus.values():
            if i == idx:
                mask_R_hippocampus |= (mask == i)
    if flatten: 
        mask_L_frontal_lobe = mask_L_frontal_lobe.flatten()
        mask_R_frontal_lobe = mask_R_frontal_lobe.flatten() 
        mask_L_temporal_lobe = mask_L_temporal_lobe.flatten()
        mask_R_temporal_lobe = mask_R_temporal_lobe.flatten() 
        mask_L_hippocampus = mask_L_hippocampus.flatten() 
        mask_R_hippocampus = mask_R_hippocampus.flatten() 
    return mask_L_frontal_lobe, mask_R_frontal_lobe, mask_L_temporal_lobe, mask_R_temporal_lobe, mask_L_hippocampus, mask_R_hippocampus



#--------------------------------------------------------------------------------------------------------------#
#                      Function to calculate the AI of the whole brain ROI or separate ROI                     #
#--------------------------------------------------------------------------------------------------------------#

# takes the output of flatten and normalize across all and left and right masks of whatever region we want
def calculate_AI(normalized_flat_data_dictionary, left_mask, right_mask):
    # dictionary to store AI as values of naccid keys
    AI_dict = defaultdict(list)
    # iterating throught whole input dictionary
    for naccid, data_array in normalized_flat_data_dictionary.items():
        # number of scans of the patient is the second dimension of this data array
        num_scans = data_array.shape[1]
        for i in range(num_scans):
            # extracting intensity values for the left and right ROI using masks
            left_hemisphere_intensity = data_array[:, i][left_mask == 1]
            right_hemisphere_intensity = data_array[:, i][right_mask == 1]
            # mean intensities
            mean_left = np.mean(left_hemisphere_intensity)
            mean_right = np.mean(right_hemisphere_intensity)
            # calculating AI for all scans
            if mean_left + mean_right != 0:
                AI = 100 * (mean_left - mean_right) / (mean_left + mean_right)
            else:
                AI = 0
            AI_dict[naccid].append(float(AI))
    return AI_dict