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

# takes already prepared flattened, normalized array of .nii data and flattened left/right masks
def calculate_AI(flat_data, left_mask, right_mask):
    # array with lenght of number of scans/patients 
    AI_array = []
    # number of scans/patients
    num_patients = flat_data.shape[1]
    for i in range(num_patients):
        # Extract the intensity values for the left and right hemispheres using the flattened masks
        left_hemisphere_intensity = flat_data[:, i][left_mask == 1]
        right_hemisphere_intensity = flat_data[:, i][right_mask == 1]
        # Calculate the mean of intensity for the left and right hemispheres
        mean_left = np.mean(left_hemisphere_intensity)
        mean_right = np.mean(right_hemisphere_intensity)
        # Calculate the asymmetry index (AI) for this patient
        if mean_left + mean_right != 0:       # Avoid division by zero
            AI = 100 * (mean_left - mean_right) / (mean_left + mean_right)
        else:
            AI = 0    
        AI_array.append(float(AI))
    return AI_array


#--------------------------------------------------------------------------------------------------------------#
#                                     TEST-RETEST REPEATABILITY FUNCTIONS                                      #
#--------------------------------------------------------------------------------------------------------------#

# relative difference
def f_RD(m1, m2):
    if (m1 + m2) != 0:
        return 100 * (m2 - m1) / ((m1 + m2)/2)
    else:
        return 0

# coefficient of variation
def f_CV(sigma, mu):
    return 100 * sigma / mu 

# within subject variation
def sigma_within(m1_array, m2_array):
    within_subject_stds = []
    for i in range(len(m1_array)):
        std = np.std([m1_array[i], m2_array[i]])
        within_subject_stds.append(std)
    return within_subject_stds

# average of two measurments
def f_mu(m1, m2):
    return (m1 + m2) / 2

# population average
def population_mu(m1_array, m2_array):
    return np.mean(m1_array + m2_array)

# between subject variation
def sigma_between(m1_array, m2_array):
    averages = []
    for i in range(len(m1_array)):
        avg = np.mean([m1_array[i], m2_array[i]])
        averages.append(avg)
    between_subject_std = np.std(averages)
    return between_subject_std


# interclass correlation coefficient
def f_ICC(sigma, sigma_b): 
    return sigma_b ** 2 / (sigma_b ** 2 + sigma ** 2)


#--------------------------------------------------------------------------------------------------------------#
#                        Using the test-retest repeatability function on my datasets                           #
#--------------------------------------------------------------------------------------------------------------#

def calculate_RD(AI_first, AI_second):
    RD_array = []
    for i in range(len(AI_first)):
        RD = f_RD(AI_first[i], AI_second[i])
        RD_array.append(float(RD))
    return RD_array


def calculate_CV(AI_first, AI_second):
    CV_array = []
    within_subject_std = sigma_within(AI_first, AI_second)
    for i in range(len(AI_first)):
        mean = f_mu(AI_first[i], AI_second[i])
        CV = f_CV(within_subject_std[i], mean)
        CV_array.append(float(CV))
    return CV_array


def calculate_ICC(AI_first, AI_second):
    ICC_array = []
    sigma_b = sigma_between(AI_first, AI_second)      # between sigma
    sigma_array = sigma_within(AI_first, AI_second)   # within sigma
    for sigma in sigma_array:
        ICC = f_ICC(sigma, sigma_b)
        ICC_array.append(float(ICC))
    return ICC_array



#--------------------------------------------------------------------------------------------------------------#
#                                   TEST-RETEST REPRODUCIBILITY FUNCTIONS                                      #
#--------------------------------------------------------------------------------------------------------------#

# means
def calculate_means(AI_first, AI_second):
    means_array = []
    for i in range(len(AI_first)):
        mean = f_mu(AI_first[i], AI_second[i])
        means_array.append(mean)
    return means_array


# difference
def f_diff(m1, m2):
    return m2 - m1

# differences array
def calculate_diffs(m1_array, m2_array):
    diffs_array = []
    for i in range(len(m1_array)):
        diff = f_diff(m2_array[i] - m1_array[i])
        diffs_array.append(diff)             
    return diffs_array      


# repeatability coefficient (1.96*std), will be used to plot repeatability coefficient 
def calculate_RC(m1_array, m2_array):
    diffs = calculate_diffs(m1_array, m2_array)
    return 1.96*np.std(diffs)

# mean difference will be plotted as solid horizontal line on Bland-Altman plots
def calculate_mean(m1_array, m2_array):
    diffs_array = calculate_diffs(m1_array, m2_array)
    mu = np.mean(diffs_array)
    return mu
                                                                    
# bias 
def f_bias(m1_array, m2_array):
    diffs_array = calculate_diffs(m1_array, m2_array)
    bias = np.mean(diffs_array)
    return bias

# limits of agreement
def f_loa(bias, sigma):
    loa = [bias + 1.96 * np.sqrt(sigma), bias - 1.96 * np.sqrt(sigma)]
    return loa