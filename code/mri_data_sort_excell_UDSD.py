#--------------------------------------------------------------------------------------------------------------#
#           Script to write common patients' IDs from two different .csv files into a new .csv file            #
#                                                                                                              #
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#


import pandas as pd

loadPath = "./NACC_data/excell/"
writePath = "./python/"
common_naccids_filepath = writePath + 'common_naccids.txt'


# reading the .csv file with UDS data
df = pd.read_csv(loadPath + 'investigator_nacc66.csv')


# Function to load NACCIDs from a .txt file
def load_common_naccids_from_txt(filepath):
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f)
    

common_naccids = load_common_naccids_from_txt(common_naccids_filepath)


# filtering data using only common NACCIDs
df_longitudinal = df[df['NACCID'].isin(common_naccids)]

# selecting relevant columns 
df_final = df_longitudinal[['NACCID', 'NACCVNUM', 'VISITMO', 'VISITDAY', 'VISITYR', 'NACCUDSD']]
df_final.columns = ['NACCID','NACCVNUM', 'VISITMO', 'VISITDAY', 'VISITYR', 'NACCUDSD']


# sanity check
print("Final dataset preview:")
print(df_final.head())


# write to a new .csv file
df_final.to_csv(writePath + 'MRIT1_longitudinal_UDS.csv', index=False)

print("Data extraction and writing to CSV complete!")