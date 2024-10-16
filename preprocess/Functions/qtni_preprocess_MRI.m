function output_file = qtni_preprocess_MRI(input_file, options)
% QTNI PET preprocessing workflow
% v1.2 - January 16th 2020
% Mauro Namías - mauro.namias@gmail.com
% This function reads a Nifti brain volume and aligns it to a template.
% input_file: raw brain image in Nifti format
% options: preprocessing options
% out_file: output file
% The end result is a 2x2x2mm brain normalized/warped to the template, with
% intensity normalization and smoothing applied. 

%Added step for segment and warp (bias correction and deformable
%registration) - May 25th 2022
%Now get 4 outputs: c1=Gray matter, c2=White matter, c3=CSF, w=whole brain

%Added step for fix origin x from 45 to 46 - June 9th 2022

% copy input file to tmp dir

temp_path = options.temp_path;

copyfile(input_file, temp_path);
disp('starting qtni_preprocess_MRI')

%% Fix coordinates
output_file = reslice_function(input_file, options);
input_file = output_file;

output_file = fix_nifti_coords_function(input_file, options);
input_file = output_file;

%% Rigid registration to template
output_file = align2templateMRI(input_file, options);
input_file = output_file;

%% segmentation 
output_file = segment_and_warpMRI(input_file, options);
%input_file = output_file;
disp('end of segmentandwarp in preprocess file')

%% Brain extraction via tissue segmentation
%output_file = extract_brain(input_file, options);

%% change origin
% input_file = output_file;
% B=load_nii(input_file);
% B.hdr.hist.qoffset_x=90;
% B.hdr.hist.srow_x=[-2,0,0,90];
% B.hdr.hist.originator=[46,64,37,0,-32768]; 
% B.original.hist.qoffset_x=90;
% B.original.hist.srow_x=[-2,0,0,90];
% B.original.hist.originator=[46,64,37,0,-32768];
% 
% slashes = strfind(input_file,'\');
% output_file=[input_file(1:slashes(end)) 'o' input_file(slashes(end)+1:end)];
% save_nii(B,output_file);


%% Output
out_path = options.out_path;

slashes = strfind(input_file,'\');
output_file1 = [input_file(1:slashes(end)) 'c1' input_file(slashes(end)+1:end)];
output_file2 = [input_file(1:slashes(end)) 'c2' input_file(slashes(end)+1:end)];
output_file3 = [input_file(1:slashes(end)) 'c3' input_file(slashes(end)+1:end)]
disp('output files created')


%% Intensity normalization (NOT USED IN EVA'S VERSION)
%switch options.intensity_norm_method
%    case 'RMS'
%        disp('Using RMS intensity normalization')
%        output_file = RMS_intensity_normalization(input_file, options);
%        input_file = output_file;
%    case 'GM'
%        disp('Using Global mean intensity normalization')
%        output_file = GM_intensity_normalization(output_file, options);
%        output_file1 = GM_intensity_normalization(output_file1, options);
%        output_file2 = GM_intensity_normalization(output_file2, options);
%        output_file3 = GM_intensity_normalization(output_file3, options);
%        %input_file = output_file;
%    case 'AAL'
%        disp('Using ROI based intensity normalization (AAL atlas)')
%        output_file = AAL_intensity_normalization(input_file, options);
%        input_file = output_file;
%    case 'NONE'
%         disp('Skipping intensity normalization')
%end

%% Finish output
copyfile(output_file, out_path);
copyfile(output_file1, out_path);
copyfile(output_file2, out_path);
copyfile(output_file3, out_path);
disp('output files copied')
delete([temp_path '\*.*']);