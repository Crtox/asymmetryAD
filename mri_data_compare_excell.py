#--------------------------------------------------------------------------------------------------------------#
#               Script to compare common patients' IDs from two different .csv files                           #
#                                                                                                              #
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#

import pandas as pd

# load and write paths 
loadPath = "./NACC_data/excell/"
writePath = "./python/"


# Step 1: Load the first CSV file (the one we created earlier)
df1 = pd.read_csv(loadPath + 'investigator_mri_nacc66.csv')

# Step 2: Load the second CSV file (the one with NACCID in the first column)
df2 = pd.read_csv(loadPath + 'investigator_nacc66.csv')

# Step 3: Extract the NACCID columns from both files
naccid_file1 = df1['NACCID'].unique()  # Extract unique NACCIDs from the first file
naccid_file2 = df2['NACCID'].unique()  # Extract unique NACCIDs from the second file

# Step 4: Find common NACCIDs in both files using set intersection
common_naccids = set(naccid_file1).intersection(set(naccid_file2))

# Step 5: Print the number of common NACCIDs and the IDs
print(f"Number of common NACCIDs: {len(common_naccids)}")
#print("Common NACCIDs:", common_naccids)

# # Optional: Save the common NACCIDs to a new CSV file if needed
# pd.DataFrame(common_naccids, columns=['NACCID']).to_csv('', index=False)

print("Comparison complete!")
