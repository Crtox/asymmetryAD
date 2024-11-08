#--------------------------------------------------------------------------------------------------------------#
#                           Script to sort MRI data by cognitive status                                        #
#                                                                                                              #
#                                    Črt Rozman, September 2024                                                #
#--------------------------------------------------------------------------------------------------------------#


import pandas as pd

loadPath = './NACC_data/sorted_cohorts/'
writePath = './python/data/'

# Load the CSV file
df = pd.read_csv(loadPath + 'trans_v3.csv')

# Group by NACCID and aggregate NACCUDSD values into a list
grouped = df.groupby('NACCID')['NACCUDSD'].apply(list)

# Initialize categories (1=normal cognition, 2=impaired-not MCI, 3=mild cognitive impairment, 4=demented)
constant_1 = []
constant_2 = []
constant_3 = []
constant_4 = []

change_1_2 = []
change_1_3 = []
change_1_4 = []
change_1_2_3 = []
change_1_2_4 = []
change_1_3_4 = []
change_1_2_3_4 = []
change_2_3 = []
change_2_4 = []
change_2_3_4 = []
change_3_4 = []

# Set to store NACCIDs that have already been categorized
categorized_naccids = set()

# Loop through each patient and categorize
for naccid, udsd_values in grouped.items():
    unique_values = list(sorted(set(udsd_values)))

    # Ensure the patient is not already categorized
    if naccid in categorized_naccids:
        continue

    # Prioritize more complex categories first
    if unique_values == [1, 2, 3, 4]:
        change_1_2_3_4.append(naccid)
    elif unique_values == [1, 2, 3]:
        change_1_2_3.append(naccid)
    elif unique_values == [1, 2, 4]:
        change_1_2_4.append(naccid)
    elif unique_values == [1, 3, 4]:
        change_1_3_4.append(naccid)
    elif unique_values == [1, 2]:
        change_1_2.append(naccid)
    elif unique_values == [1, 3]:
        change_1_3.append(naccid)
    elif unique_values == [1, 4]:
        change_1_4.append(naccid)
    elif unique_values == [2, 3, 4]:
        change_2_3_4.append(naccid)
    elif unique_values == [2, 3]:
        change_2_3.append(naccid)
    elif unique_values == [2, 4]:
        change_2_4.append(naccid)
    elif unique_values == [3, 4]:
        change_3_4.append(naccid)
    
    # Now handle constant values
    elif unique_values == [1]:
        constant_1.append(naccid)
    elif unique_values == [2]:
        constant_2.append(naccid)
    elif unique_values == [3]:
        constant_3.append(naccid)
    elif unique_values == [4]:
        constant_4.append(naccid)

    # Mark this patient as categorized
    categorized_naccids.add(naccid)


# Sanity check: Ensure no duplication across categories
total_count = (
    len(constant_1) + len(constant_2) + len(constant_3) + len(constant_4) +
    len(change_1_2) + len(change_1_3) + len(change_1_4) +
    len(change_1_2_3) + len(change_1_2_4) + len(change_1_3_4) +
    len(change_1_2_3_4) + len(change_2_3) + len(change_2_4) +
    len(change_2_3_4) + len(change_3_4)
)

print(f"Total number of NACCIDs across all categories: {total_count}")


# Save results to a .txt file
with open(writePath + 'trans_uds_categories.txt', 'w') as f:
    # Write each group into a new row
    f.write(",".join(constant_1) + '\n')
    f.write(",".join(constant_2) + '\n')
    f.write(",".join(constant_3) + '\n')
    f.write(",".join(constant_4) + '\n')
    f.write(",".join(change_1_2) + '\n')
    f.write(",".join(change_1_3) + '\n')
    f.write(",".join(change_1_4) + '\n')
    f.write(",".join(change_1_2_3) + '\n')
    f.write(",".join(change_1_2_4) + '\n')
    f.write(",".join(change_1_3_4) + '\n')
    f.write(",".join(change_1_2_3_4) + '\n')
    f.write(",".join(change_2_3) + '\n')
    f.write(",".join(change_2_4) + '\n')
    f.write(",".join(change_2_3_4) + '\n')
    f.write(",".join(change_3_4) + '\n')

print("NACCID categorization complete and saved to .txt file!")
