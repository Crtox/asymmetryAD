#--------------------------------------------------------------------------------------------------------------#
#                                     Script to preprocess .nii files                                          #
#                                                                                                              #
#                                         Črt Rozman, October 2024                                             #
#                                                                                                              #
#                      Rewritten from Matlab code that was written by Mauro Namies in 2020                     #
#--------------------------------------------------------------------------------------------------------------#



# Importing needed modules
import os
import time
from glob import glob
from tqdm import tqdm  # For progress bar


# Configure options as a dictionary
options = {
    'temp_path': 'C:/Users/Crt/Desktop/WIMR/asymmetryAD/python/preprocess/temp/',  # Temporary file storage
    'TPM_path': 'C:/Users/Crt/Desktop/WIMR/asymmetryAD/python/preprocess/Templates/TPM.nii',  # Tissue probability map path
    'out_path': 'C:/Users/Crt/Desktop/WIMR/asymmetryAD/NACC_data/sorted_cohorts_preprocessed/',  # Output directory
    'PET_template': 'C:/Users/Crt/Desktop/WIMR/asymmetryAD/python/preprocess/Templates/single_subj_T1.nii',  # Brain template for normalization
    'PET_atlas': 'C:/Users/Crt/Desktop/WIMR/asymmetryAD/python/preprocess/Templates/AAL3+Pons\AAL3+pons.nii',  # Atlas for normalization
    'intensity_norm_method': 'GM',  # Intensity normalization method
    # 'intensity_norm_regions': list(range(95, 121)) + [171],  # Uncomment if needed
    'SmoothFWHM': 0,  # Smoothing parameter
    'use_oldnorm': 0  # Use SPM5 or SPM12 spatial normalization
}


# Directory containing original nifti files
input_dir = 'C:/Users/Crt/Desktop/WIMR/asymmetryAD/NACC_data/sorted_cohorts/'

# Function placeholder for qtni_preprocess_MRI_wSkullStrip_noTemplate
def qtni_preprocess_MRI_wSkullStrip_noTemplate(input_file, options):
  
    output_file = os.path.join(options['out_path'], os.path.basename(input_file))  # Output path example

    return output_file

# Read all files in the input directory
files = glob(os.path.join(input_dir, '*.nii'))  # Assuming input files are in NIfTI format

# Progress bar for file processing
for i in tqdm(range(len(files)), desc="Processing files"):
    start_time = time.time()
    input_file = files[i]  # Get the file path
    output_file = qtni_preprocess_MRI_wSkullStrip_noTemplate(input_file, options)  # Process the file
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate time for the iteration
    print(f"Processed {os.path.basename(input_file)} in {elapsed_time:.2f} seconds")

print("All files processed successfully.")