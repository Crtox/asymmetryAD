# File for quick testing and sanity checks

import pandas as pd
import os 

matching_folders = ['//?/c:/Users/Crt/Desktop/WIMR/asymmetryAD/NACC_data/sorted_cohorts/MCI/mri8189ni']

# Regular expression for T1 subfolder
T1_prefix = 'T1'
nacc_prefix = 'NACC'
mprage_prefix = 'MPRAGE'
fspgr_prefix = 'FSPGR'


# Loop through each folder in matching_folders
for folder in matching_folders:

    # List all subfolders in the folder_path
    subfolders = os.listdir(folder)
    
    # Folders that contain only 1 subfolder (those have different substructures)
    if len(subfolders) == 1:

        subfolder_full_path = os.path.join(folder, subfolders[0])                        # only one subfolder 

        if os.path.isdir(subfolder_full_path) and subfolders[0].startswith(nacc_prefix):

            subfolders_in_nacc = os.listdir(subfolder_full_path)                         # List subfolders inside NACC (either nacc or many subfolders)

            if len(subfolders_in_nacc) == 1:                                             # Some have structure NACC--->nacc--->subfolders like MPRAGE, FSPGR
                
                subfolder_in_nacc_full_path = os.path.join(subfolder_full_path, subfolders_in_nacc[0])         # only one subfolder
 
                subfolders_in_subfolder_nacc_in_nacc = os.listdir(subfolder_in_nacc_full_path)

                for subs in subfolders_in_subfolder_nacc_in_nacc: 

                    print(subs)