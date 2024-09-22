#--------------------------------------------------------------------------------------------------------------#
#               Script to compare common patients' IDs from two different .csv files                           #
#                                                                                                              #
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#

import pandas as pd

# load and write paths 
loadPath1 = "./NACC_data/excell/"
loadPath2 = "./python/"


# Step 1: Load the first CSV file (the one we created earlier)
df1 = pd.read_csv(loadPath1 + 'investigator_nacc66.csv')

# Step 2: Load the second CSV file (the one with NACCID in the first column)
df2 = pd.read_csv(loadPath2 + 'MRIT1_longitudinal.csv')

# Step 3: Extract the NACCID columns from both files
naccid_file1 = df1['NACCID'].unique()  # Extract unique NACCIDs from the first file
naccid_file2 = df2['NACCID'].unique()  # Extract unique NACCIDs from the second file

# Step 4: Find common NACCIDs in both files using set intersection
common_naccids = set(naccid_file1).intersection(set(naccid_file2))

# Step 5: Print the number of common NACCIDs and the IDs
print(f"Number of common NACCIDs: {len(common_naccids)}")

print("Comparison complete!")


####################################################################################################################################
#CONCLUSION: all the longitudinal data from investigator_mri_nacc66 (I stored in MRIT1_longitudinal) is also in investigator_nacc66#
####################################################################################################################################


# Now I will take all the common NACCIDs and write them to a new .csv file that includes all the UDS visits data

writePath = "./python/"

# filtering data using only common NACCIDs
df_longitudinal = df2[df2['NACCID'].isin(common_naccids)]

# selecting relevant columns 
df_final = df_longitudinal[['NACCID'], ['NACCVNUM'], ['VISITMO'], ['VISITDAY'], ['VISITYR'], ['NACCUDSD']]
df_final.columns = ['NACCID'], ['NACCVNUM'], ['VISITMO'], ['VISITDAY'], ['VISITYR'], ['NACCUDSD']


# sanity check
print("Final dataset preview:")
print(df_final.head())


# write to a new .csv file
df_final.to_csv(writePath + 'MRIT1_longitudinal_UDS.csv', index=False)

print("Data extraction and writing to CSV complete!")