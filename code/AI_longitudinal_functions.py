#--------------------------------------------------------------------------------------------------------------#
#                       Script to store functions used in "AI_longitudinal.ipynb"                              #
#                                                                                                              #
#                                      Črt Rozman, October 2024                                                #
#--------------------------------------------------------------------------------------------------------------#

import os 
import re
import numpy as np
from dateutil import parser
from collections import defaultdict
import nibabel as nib
import matplotlib.pyplot as plt



#--------------------------------------------------------------------------------------------------------------#
#        Function to count how many different patients we have and how many scans each of them has.            #
#--------------------------------------------------------------------------------------------------------------#