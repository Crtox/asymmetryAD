function output_file = oldnorm(input_file, options);
% output_file = oldnorm(input_file, options);
% Performs Affine-based + DCT spatial normalization to a template (SPM5 or
% "old normalization".
% v1.0 , November 2019, Mauro Namías, mauro.namias@gmail.com

TPM_path = options.TPM_path; % Tissue probability map
temp_path = options.temp_path;
template_path = options.PET_template;
files_cell = [];
files_cell{1} = [input_file, ',1'];
   
% Configure SPM job for spatial norm
clear matlabbatch
matlabbatch{1}.spm.tools.oldnorm.estwrite.subj.source = {files_cell{1}};
matlabbatch{1}.spm.tools.oldnorm.estwrite.subj.wtsrc = '';
matlabbatch{1}.spm.tools.oldnorm.estwrite.subj.resample = {files_cell{1}};
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.template = {[template_path ',1']};
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.weight = '';
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.smosrc = 8;
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.smoref = 0;
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.regtype = 'mni';
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.cutoff = 25;
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.nits = 16;
matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.reg = 1; 
matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.preserve = 0;
matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.bb = [-92 -126 -72
                                                         88 90 108];
matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.vox = [2 2 2];
matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.interp = 4;
matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.wrap = [0 0 0];
matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.prefix = 'w';

% Run SPM job
nrun = 1; % enter the number of runs here
inputs = cell(0, nrun);
spm_jobman('initcfg');
spm('defaults', 'PET');
spm_jobman('run',matlabbatch,inputs(:));

delete([temp_path '\*.mat']);
delete([temp_path '\y*.nii']);

slashes = strfind(input_file,'\');
output_file = [input_file(1:slashes(end)) 'w' input_file(slashes(end)+1:end)];

