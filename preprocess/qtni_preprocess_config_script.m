%% QTNI for MRI preprocess main script
% v1.3 January 29th 2020
% Mauro Namías - mauro.namias@gmail.com
% This scripts configures and runs the QTNI MRI pre-processing workflow, i.e.:
% spatial normalization to the MNI space, using SPM template.

% v1.4 May 25th 2022
% added step for segment and warp, which bias correct and deformable
% register MRI images

%WITH OR WITHOUT Skull Stripping dependent on which qtni_preprocess file
%you call ("_MRI_wSkullStrip")


%%NOTE: Files must be in .nii format. If in .nii.gz, use gunzip to
%%extract them. Using 7zip or other manual unzippers will change the name
%%of the file.
%Navigate to the directory and type "gunzip -r ." (with the period)

%Notes:
    %%Only add to path folders that you actually want to use. Make sure you
    %don't have any old versions of qnti in the path.
    %%Make sure the temp folder is empty when you start the config script

cfolder = 'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\';
path(path,cfolder)
path(path,[cfolder '\Functions\'])



% Configure options
options.temp_path = 'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\temp\'  % Directory to store temporal files (which are deleted once the script is finished)
options.TPM_path = 'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\Templates\TPM.nii'; % Tissue probability map for brain segmentation and spatial normalization
options.out_path = 'C:\Users\deatsch\Documents\MATLAB\qtni_preprocessed\';  % Output directory, where normalized files are stored
options.PET_template = 'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\Templates\single_subj_T1.nii';  % FDG (or any other) brain template for non-linear spatial normaliaztion
options.PET_atlas = 'C:\Users\deatsch\Documents\MATLAB\QTNI_MRI_preprocess_v1.5\Templates\AAL3+Pons\AAL3+pons.nii';
options.intensity_norm_method = 'GM'; % Select either 'GM' (global mean), 'RMS', 'AAL' or 'NONE'. The AAL option allows to select reference regions for normalization (see example in the next line)
% options.intensity_norm_regions = [95:120 171]; % list of AAL regions used for intensity normalization. In this example, the cerebellum and the pons are used. See the \Templates\AAL+pons\AAL3.txt file for the list of region codes
options.SmoothFWHM = 0;  % FWHM of the 3D Gaussian kernel used for smoothing
options.use_oldnorm = 0;  % Use SPM5 spatial normalization (affine + DCT) instead of SPM12 spatial norm (segmentation + warping).


input_dir = 'C:\Users\deatsch\Documents\MATLAB\qtni_input';  % Directory containing all original nifti files

files = dir(input_dir);

progressbar()

    for i = 3:length(files) 
    tic
    input_file = [input_dir '\' files(i).name];
    output_file = qtni_preprocess_MRI_wSkullStrip_noTemplate(input_file, options);    
    progressbar(i/(length(files) ));
    toc
    end



   