function output_file = align2templateMRI(input_file, options);
% function output_file = align2template(input_file, options);
% Rigid registration to a template 
% v1.0 , November 2019, Mauro Namías, mauro.namias@gmail.com

temp_path = options.temp_path;

files_cell{1} = [input_file ',1'];
    


   
% Configure SPM job 
clear matlabbatch
ref = [options.PET_template ',1']
matlabbatch{1}.spm.spatial.coreg.estwrite.ref = {ref};
matlabbatch{1}.spm.spatial.coreg.estwrite.source =  {files_cell{1}};
matlabbatch{1}.spm.spatial.coreg.estwrite.other = {files_cell{1}};                                                 
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.interp = 4;
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.mask = 0;
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.prefix = 'cr';


% Run SPM batch
nrun = 1; % enter the number of runs here
inputs = cell(0, nrun);
spm_jobman('initcfg');
spm('defaults', 'PET');
spm_jobman('run',matlabbatch,inputs(:))

%delete([temp_path '\*.mat']);
%delete(input_file);
%delete([temp_path '\y*.nii']);


file_list = dir(temp_path);
filenames = {file_list.name};
file_indexes = strfind(filenames,'cr');

for i = 1:length(file_indexes)
    index = cell2mat(file_indexes(i));
    if(isempty(index))
    else
    fname = filenames(i)
    output_file = [temp_path, cell2mat(fname)]  
    end    
end


% output_file = [temp_path '\' filename];

