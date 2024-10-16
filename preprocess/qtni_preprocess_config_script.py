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
    'temp_path': r'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\temp\\',  # Temporary file storage
    'TPM_path': r'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\Templates\TPM.nii',  # Tissue probability map path
    'out_path': r'C:\Users\deatsch\Documents\MATLAB\qtni_preprocessed\\',  # Output directory
    'PET_template': r'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\Templates\single_subj_T1.nii',  # Brain template for normalization
    'PET_atlas': r'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\Templates\AAL3+Pons\AAL3+pons.nii',  # Atlas for normalization
    'intensity_norm_method': 'GM',  # Intensity normalization method
    # 'intensity_norm_regions': list(range(95, 121)) + [171],  # Uncomment if needed
    'SmoothFWHM': 0,  # Smoothing parameter
    'use_oldnorm': 0  # Use SPM5 or SPM12 spatial normalization
}


# Directory containing original nifti files
input_dir = r'C:\Users\deatsch\Documents\MATLAB\qtni_input'

# Function placeholder for qtni_preprocess_MRI_wSkullStrip_noTemplate
# You will need to implement this function according to your MRI preprocessing logic
def qtni_preprocess_MRI_wSkullStrip_noTemplate(input_file, options):
    # Preprocessing logic would go here. The function will process the MRI data
    # based on the input file and options, and return an output file.
    # Implement the required steps like segmentation, skull stripping, etc.
    output_file = os.path.join(options['out_path'], os.path.basename(input_file))  # Output path example
    # You can integrate real processing logic here.
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