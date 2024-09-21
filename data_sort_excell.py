#--------------------------------------------------------------------------------------------------------------#
#        Script to filter out relevant data from given excell files and write it to a new excell file          #
#                                   
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#

import pandas as pd

# load and write paths 
loadPath = "../NACC_data/excell/"
writePath = "./"

# Load the Excel file
df = pd.read_csv(loadPath+'investigator_mri_nacc66.csv', engine='openpyxl')

# Filter only patients with MRIT1 = 1 (those who had their MRIT1 taken)
df_mri_t1 = df[df['MRIT1'] == 1]

# Step 3: Find patients (NACCID) that occur more than twice, meaning they had multiple scans
# We use `value_counts` to find NACCIDs with more than one scan.
multiple_scans = df_mri_t1['NACCID'].value_counts()
multiple_scans = multiple_scans[multiple_scans > 1].index

# Filter the data to include only those patients with multiple scans
df_longitudinal = df_mri_t1[df_mri_t1['NACCID'].isin(multiple_scans)]

# Create a new column for the combined date (MRIMO/MRIDY/MRIYR) as "MM/DD/YYYY"
df_longitudinal['MRIDate'] = df_longitudinal['MRIMO'].astype(str) + '/' + df_longitudinal['MRIDY'].astype(str) + '/' + df_longitudinal['MRIYR'].astype(str)

# Select only the columns we need and rename them according to the new file structure
df_final = df_longitudinal[['NACCID', 'NACCMNUM', 'MRIDate', 'NACCMRIA', 'NACCMRFI']]
df_final.columns = ['NACCID', 'NACCMNUM', 'MRIMO/MRIDY/MRIYR', 'NACCMRIA', 'NACCMRFI']

# Write the filtered and formatted data to a new Excel file
df_final.to_csv(writePath+'MRIT1_longitudinal.xlsx', index=False, engine='xlsxwriter')

print("Data extraction and writing complete!")