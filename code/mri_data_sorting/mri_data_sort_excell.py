#--------------------------------------------------------------------------------------------------------------#
#        Script to filter out relevant data from given excell files and write it to a new excell file          #
#                                                                                                              #
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#

import pandas as pd

# load and write paths 
loadPath = "./NACC_data/excell/"
writePath = "./python/data/"



# Load the CSV file
df = pd.read_csv(loadPath + 'investigator_mri_nacc66.csv')

# Filter only patients with MRIT1 = 1 (those who had their MRIT1 taken)
df_mri_t1 = df[df['MRIT1'] == 1]

# Find patients (NACCID) that occur more than twice, meaning they had multiple scans
# We use `value_counts` to find NACCIDs with more than one scan.
multiple_scans = df_mri_t1['NACCID'].value_counts()
multiple_scans = multiple_scans[multiple_scans > 1].index

# Filter the data to include only those patients with multiple scans
df_longitudinal = df_mri_t1[df_mri_t1['NACCID'].isin(multiple_scans)]


# # NEW IMPLEMENTATION 
# #---------------------------------------------------------------------------#
# common_naccids_filepath = writePath + 'naccids_common_ALZD.txt'

# # Function to load NACCIDs from a .txt file
# def load_common_naccids_from_txt(filepath):
#      with open(filepath, 'r') as f:
#          return set(line.strip() for line in f)
    

# common_naccids = load_common_naccids_from_txt(common_naccids_filepath)

# filtering data using only common NACCIDs
#df_longitudinal = df[df['NACCID'].isin(common_naccids)]
# #---------------------------------------------------------------------------#


# Select only the relevant columns and rename them according to the new file structure
df_final = df_longitudinal[['NACCID', 'NACCMNUM', 'MRIMO', 'MRIDY', 'MRIYR', 'NACCMRIA', 'NACCMRFI']]
df_final.columns = ['NACCID', 'NACCMNUM', 'MRIMO', 'MRIDY', 'MRIYR', 'NACCMRIA', 'NACCMRFI']

# Debugging: Check the final dataset before saving
print("Final dataset preview:")
print(df_final.head())

# Write the filtered and formatted data to a new CSV file
df_final.to_csv(writePath + 'MRIT1_longitudinal.csv', index=False)

print("Data extraction and writing to CSV complete!")


