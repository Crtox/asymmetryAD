function output_file = qtni_preprocess(input_file, options)
% QTNI PET preprocessing workflow
% v1.2 - January 16th 2020
% Mauro Namías - mauro.namias@gmail.com
% This function reads a Nifti brain volume and aligns it to a template.
% input_file: raw brain image in Nifti format
% options: preprocessing options
% out_file: output file
% The end result is a 2x2x2mm brain normalized/warped to the template, with
% intensity normalization and smoothing applied. 

% copy input file to tmp dir

temp_path = options.temp_path;

copyfile(input_file, temp_path);

%% Rigid registration to template
output_file = align2template(input_file, options);
input_file = output_file;

%% Brain extraction via tissue segmentation
output_file = extract_brain(input_file, options);
input_file = output_file;

%% Spatial Normalization (Affine + deformable registration) to template (SPM5 old norm) or TPM (SPM12)
if(options.use_oldnorm)
    output_file = oldnorm(input_file, options);
    input_file = output_file;
else
    output_file = segment_and_warp(input_file, options);
    input_file = output_file;
end

%% Intensity normalization
switch options.intensity_norm_method
    case 'RMS'
        disp('Using RMS intensity normalization')
        output_file = RMS_intensity_normalization(input_file, options);
        input_file = output_file;
    case 'GM'
        disp('Using Global mean intensity normalization')
        output_file = GM_intensity_normalization(input_file, options);
        input_file = output_file;
    case 'AAL'
        disp('Using ROI based intensity normalization (AAL atlas)')
        output_file = AAL_intensity_normalization(input_file, options);
        input_file = output_file;
    case 'NONE'
         disp('Skipping intensity normalization')
end



%% Smoothing
output_file = smooth_brain(input_file, options);
out_path = options.out_path;

copyfile(output_file, out_path);
delete([temp_path '\*.*']);

