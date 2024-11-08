# 🧠 asymmetryAD

[![Python Version](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/downloads/)

## 📖 Project Overview

**asymmetryAD** is a Python-based project focused on Alzheimer's Disease (AD) research. This repository contains code and results generated during my work at the **Wisconsin Institutes for Medical Research (WIMR)** in Madison, WI. The project runs from **September 2nd to November 18th, 2024**.

## 🔍 Research Goals

1. **Validate Results**: 
   - Reproduce and evaluate findings from previous studies on new data.
   
2. **Biomarker Development**:
   - Investigate and design new biomarkers to detect asymmetry in Alzheimer's Disease, potentially offering more robust diagnostic tools.

3. **Result correlation**:
   - Correlate physician’s observations in asymmetry with freshly produces results

## 🛠️ Tech Stack

- **Programming Language**: Python 🐍
- **Libraries**: 
   - `numpy`, `scipy`, `nibabel`, `matplotlib`, `pandas`, etc.
   - Specialized packages for medical image processing and statistical analysis.
   
## 📁 Repository Structure

```bash
asymmetryAD/
│
├── code/                            # Python scripts for calculation, sorting and analyzing 
├── results/                         # Output files and results of experiments
└── README.md                        # This file!

Repository Explanation:
Inside of code/ repository you can find all the code I've written. Main scripts are:
   - AI_longitudinal: man script for all my longitudinal analysis
   - AI_longitudinal_functions: all the functions called and used in AI_longitudinal script
   - test_retest: main script for the test-retest study
   - test_retest_functions: functions used and called in test_retest script
   - NACC_data_sorting: scripts for sorting the dataset from NACC (not important for you)

Inside of results/ repository you can find different plots, results and .csv files I produced with my code scripts. Main results folder are:
   - NACC_data_sorting: look at final folder, inside are 4 .csv files that contain info on    
     patients' scans in cohorts of data I worked with in longitudinal analysis
   - AI_longitudinal: you can find plots from longitudinal analysis here
   - test_retest: you can find plots from test-retest study here
