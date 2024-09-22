#--------------------------------------------------------------------------------------------------------------#
#        Script to filter out relevant data from given excell files and write it to a new excell file          #
#                                   
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#

import pandas as pd

# load and write paths 
loadPath = "./NACC_data/excell/"
writePath = "./python/"



# Step 1: Load the CSV file
df = pd.read_csv(loadPath + 'investigator_mri_nacc66.csv')

# Step 2: Filter only patients with MRIT1 = 1 (those who had their MRIT1 taken)
df_mri_t1 = df[df['MRIT1'] == 1]

# Step 3: Find patients (NACCID) that occur more than twice, meaning they had multiple scans
# We use `value_counts` to find NACCIDs with more than one scan.
multiple_scans = df_mri_t1['NACCID'].value_counts()
multiple_scans = multiple_scans[multiple_scans > 1].index

# Step 4: Filter the data to include only those patients with multiple scans
df_longitudinal = df_mri_t1[df_mri_t1['NACCID'].isin(multiple_scans)]

# Step 5: Select only the relevant columns and rename them according to the new file structure
df_final = df_longitudinal[['NACCID', 'NACCMNUM', 'MRIMO', 'MRIDY', 'MRIYR', 'NACCMRIA', 'NACCMRFI']]
df_final.columns = ['NACCID', 'NACCMNUM', 'MRIMO', 'MRIDY', 'MRIYR', 'NACCMRIA', 'NACCMRFI']

# Debugging: Check the final dataset before saving
print("Final dataset preview:")
print(df_final.head())

# Step 6: Write the filtered and formatted data to a new CSV file
df_final.to_csv(writePath + 'MRIT1_longitudinal.csv', index=False)

print("Data extraction and writing to CSV complete!")