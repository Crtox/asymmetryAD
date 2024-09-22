#--------------------------------------------------------------------------------------------------------------#
#                           Script to sort MRI data by cognitive status                                        #
#                                                                                                              #
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#



import pandas as pd

writePath = './python/'


# Load the CSV file
df = pd.read_csv('path_to_your_csv/MRIT1_longitudinal_UDS.csv')


# Group by NACCID and aggregate NACCUDSD values into a list
grouped = df.groupby('NACCID')['NACCUDSD'].apply(list)


# Initialize categories (1=normal cognition, 2=impaired-not MCI, 3=mild cognitive impairment, 4=demented)
constant_1 = []
constant_2 = []
constant_3 = []
constant_4 = []
change_1_2 = []
change_2_3 = []
change_3_4 = []
change_1_2_3 = []
change_2_3_4 = []


# Loop through each patient and categorize
for naccid, udsd_values in grouped.items():
    unique_values = list(sorted(set(udsd_values)))
    
    # Constant values
    if unique_values == [1]:
        constant_1.append(naccid)
    elif unique_values == [2]:
        constant_2.append(naccid)
    elif unique_values == [3]:
        constant_3.append(naccid)
    elif unique_values == [4]:
        constant_4.append(naccid)
    
    # Changes in values
    elif unique_values == [1, 2]:
        change_1_2.append(naccid)
    elif unique_values == [2, 3]:
        change_2_3.append(naccid)
    elif unique_values == [3, 4]:
        change_3_4.append(naccid)
    elif unique_values == [1, 2, 3]:
        change_1_2_3.append(naccid)
    elif unique_values == [2, 3, 4]:
        change_2_3_4.append(naccid)

        

# Save results to a .txt file
with open(writePath + 'naccids_by_uds_categories.txt', 'w') as f:
    # Write each group into a new row
    f.write(",".join(constant_1) + '\n')
    f.write(",".join(constant_2) + '\n')
    f.write(",".join(constant_3) + '\n')
    f.write(",".join(constant_4) + '\n')
    f.write(",".join(change_1_2) + '\n')
    f.write(",".join(change_2_3) + '\n')
    f.write(",".join(change_3_4) + '\n')
    f.write(",".join(change_1_2_3) + '\n')
    f.write(",".join(change_2_3_4) + '\n')

print("NACCID categorization complete and saved to .txt file!")