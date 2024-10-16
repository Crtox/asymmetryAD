function output_file = smooth_brain(input_file, options);
% function output_file = smooth_brain(input_file, options);
% Smooths the brain with a 3D Gaussian kernel
% v1.0 , November 2019, Mauro Namías - mauro.namias@gmail.com

TPM_path = options.TPM_path; % Tissue probability map
temp_path = options.temp_path;
FWHM = options.SmoothFWHM;
files_cell = [];
files_cell{1} = [input_file, ',1'];

  
%Configure SPM job 
clear matlabbatch
matlabbatch{1}.spm.spatial.smooth.data = {files_cell{1}};
matlabbatch{1}.spm.spatial.smooth.fwhm = [FWHM FWHM FWHM];
matlabbatch{1}.spm.spatial.smooth.dtype = 0;
matlabbatch{1}.spm.spatial.smooth.im = 0;
matlabbatch{1}.spm.spatial.smooth.prefix = 's';

% Run SPM job
nrun = 1; % enter the number of runs here
inputs = cell(0, nrun);
spm_jobman('initcfg');
spm('defaults', 'PET');
spm_jobman('run',matlabbatch,inputs(:))

slashes = strfind(input_file,'\');
output_file = [input_file(1:slashes(end)) 's' input_file(slashes(end)+1:end)];

