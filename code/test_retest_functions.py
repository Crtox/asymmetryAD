#--------------------------------------------------------------------------------------------------------------#
#                        Script to store functions used in "test-retes.ipynb"                                  #
#                                                                                                              #
#                                    Črt Rozman, October 2024                                                  #
#--------------------------------------------------------------------------------------------------------------#

import os 
import re
import numpy as np
from dateutil import parser
from collections import defaultdict
import nibabel as nib
import matplotlib.pyplot as plt


#--------------------------------------------------------------------------------------------------------------#
#        Function to count how many different patients we have and how many scans each of them has.            #
#--------------------------------------------------------------------------------------------------------------#

def count_patients_scans_helper(folder_path, pattern):
    patient_scans = defaultdict(int)
    # Loop through all the files in the folder
    for filename in os.listdir(folder_path):
        # Search for the patient ID in the filename
        match = pattern.search(filename)
        if match:
            patient_id = match.group(1)  # Extract patient ID
            # Increment the count for this patient
            patient_scans[patient_id] += 1
    return patient_scans


def count_patients_scan(fspgr_folder_path, mprage_folder_path):
    # Regular expression to find the patient ID in filenames
    fspgr_pattern = re.compile(r'c1bet_crf_rsl_([A-Z0-9]{6})')  # FSPGR patient ID pattern
    mprage_pattern = re.compile(r'c1bet_crf_rsl_(S[0-9]{3})')   # MPRAGE patient ID pattern
    # Use the helper function to count scans in both folders
    fspgr_patient_scans = count_patients_scans_helper(fspgr_folder_path, fspgr_pattern)
    mprage_patient_scans = count_patients_scans_helper(mprage_folder_path, mprage_pattern)
    return fspgr_patient_scans, mprage_patient_scans




#--------------------------------------------------------------------------------------------------------------#
#         Function that creates a dictionary with patient ID as keys and their scan dates as values.           #
#--------------------------------------------------------------------------------------------------------------#

def date_of_scans_helper(folder_path, pattern, date_pattern, patient_scans):    
    # empty dictionary to store patient dates, dictionary with empty list as value
    patient_dates = defaultdict(list)
    # iterating throught all files in folder
    for filename in os.listdir(folder_path):
        # finding match with pattern
        match = pattern.search(filename)
        if match:
            # extracting patient ID
            patient_id = match.group(1)
            # only looking at those patient with 2 scans
            if patient_id in patient_scans:
                date_match = date_pattern.search(filename)
                if date_match:
                    patient_dates[patient_id].append(date_match.group(0))
    return patient_dates 


def date_of_scans(fspgr_folder_path, patient_scans):
    # regular expression for ID and date format
    fspgr_pattern = re.compile(r'c1bet_crf_rsl_([A-Z0-9]{6})')
    fspgr_date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    fspgr_dates = date_of_scans_helper(fspgr_folder_path, fspgr_pattern, fspgr_date_pattern, patient_scans)
    return fspgr_dates




#--------------------------------------------------------------------------------------------------------------#
#         Function that stores the paths of the .nii files for easier access later on                          #
#--------------------------------------------------------------------------------------------------------------#

def filepaths_helper(folder, pattern, patient_scans): 
    # storing the file paths in an empty array
    fp = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        match = pattern.search(filename)
        if match: 
            patient_id = match.group(1)
            if patient_id in patient_scans:
                fp.append(filepath)
    return fp


def filepaths(fspgr_folder, mprage_folder, patient_scans):
    fspgr_pattern = re.compile(r'wbet_crf_rsl_([A-Z0-9]{6})')
    mprage_pattern = re.compile(r'wbet_crf_rsl_(S[0-9]{3})')
    fspgr_files = filepaths_helper(fspgr_folder, fspgr_pattern, patient_scans)
    mprage_files = filepaths_helper(mprage_folder, mprage_pattern, patient_scans)
    return fspgr_files, mprage_files




#--------------------------------------------------------------------------------------------------------------#
#                     Function that separates first scans from the second scans                                #
#--------------------------------------------------------------------------------------------------------------#

def separate_scans(files):
    first_scans = []
    second_scans = []
    for i in range(len(files)): 
        if i % 2 == 0:                     # even index is first scan, odd is second scan
            first_scans.append(files[i])
        else: 
            second_scans.append(files[i])
    return first_scans, second_scans




#--------------------------------------------------------------------------------------------------------------#
#              Function to prepare patient data: flatten 3D array to 1D and normalize by intensity             #
#--------------------------------------------------------------------------------------------------------------#

def flatten_and_normalize(nii_files, mask=False):
    flat_nii_files = []                 # array to store flattened files
    for nii_file in nii_files:
        img = nib.load(nii_file) 
        img_data = img.get_fdata()       # extracting data
        img_1d = img_data.flatten()      # flattening array
        flat_nii_files.append(img_1d)
    # transform into numpy array, where each column is patients data
    flat_nii_files = np.column_stack(flat_nii_files)
    # normalize if we are dealing with patients data
    if not mask:
        normalized_flat_nii_files = flat_nii_files / np.sum(flat_nii_files, axis=0)
    # no need to normalize if we are dealing with mask
    return normalized_flat_nii_files



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


def mask_hemispheres(mask_path, mask_txt_file):
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
    left_hemisphere_mask = left_hemisphere_mask.flatten()   
    right_hemisphere_mask = right_hemisphere_mask.flatten()
    return left_hemisphere_mask, right_hemisphere_mask