function output_file = extract_brain(input_file, options);
% function output_file = extract_brain(input_file, options);
% Segments the skull based on a tissue probability map, and then keep just
% the brain
% v1.0 , November 2019, Mauro Namías, mauro.namias@gmail.com
disp('start of extract brain')

TPM_path = options.TPM_path; % Tissue probability map
temp_path = options.temp_path;

files_cell = []
files_cell{1} = [input_file, ',1'];


   
% Configure SPM job for tissue segmentation
clear matlabbatch
%matlabbatch{1}.spm.spatial.preproc.channel.vols = {'F:\Documentos\Doctorado\Posibles papers\Melanoma\Images\Brains per patient\M08\00_Original\rM08_1.img,1'};
matlabbatch{1}.spm.spatial.preproc.channel.vols = {files_cell{1}};
matlabbatch{1}.spm.spatial.preproc.channel.biasreg = 0;
matlabbatch{1}.spm.spatial.preproc.channel.biasfwhm = 60;
matlabbatch{1}.spm.spatial.preproc.channel.write = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(1).tpm = {[TPM_path ',1']};
matlabbatch{1}.spm.spatial.preproc.tissue(1).ngaus = 1;
matlabbatch{1}.spm.spatial.preproc.tissue(1).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(1).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(2).tpm = {[TPM_path ',2']};
matlabbatch{1}.spm.spatial.preproc.tissue(2).ngaus = 1;
matlabbatch{1}.spm.spatial.preproc.tissue(2).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(2).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(3).tpm = {[TPM_path ',3']};
matlabbatch{1}.spm.spatial.preproc.tissue(3).ngaus = 2;
matlabbatch{1}.spm.spatial.preproc.tissue(3).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(3).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(4).tpm = {[TPM_path ',4']};
matlabbatch{1}.spm.spatial.preproc.tissue(4).ngaus = 3;
matlabbatch{1}.spm.spatial.preproc.tissue(4).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(4).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(5).tpm = {[TPM_path ',5']};
matlabbatch{1}.spm.spatial.preproc.tissue(5).ngaus = 4;
matlabbatch{1}.spm.spatial.preproc.tissue(5).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(5).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(6).tpm = {[TPM_path ',6']};
matlabbatch{1}.spm.spatial.preproc.tissue(6).ngaus = 2;
matlabbatch{1}.spm.spatial.preproc.tissue(6).native = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(6).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.warp.mrf = 1;
matlabbatch{1}.spm.spatial.preproc.warp.cleanup = 1;
matlabbatch{1}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];
matlabbatch{1}.spm.spatial.preproc.warp.affreg = 'mni';
matlabbatch{1}.spm.spatial.preproc.warp.fwhm = 2;
matlabbatch{1}.spm.spatial.preproc.warp.samp = 3;
matlabbatch{1}.spm.spatial.preproc.warp.write = [0 0];


% Run SPM tissue segmentation
nrun = 1; % enter the number of runs here
inputs = cell(0, nrun);
spm_jobman('initcfg');
spm('defaults', 'PET');
spm_jobman('run',matlabbatch,inputs(:))

% Search the segmented binary masks
filelist = dir(temp_path)
indexes = strfind({filelist.name},'.nii');
indexes_ok = find(~cellfun(@isempty, indexes));

indexes = strfind({filelist.name},'c');
indexes_bet = find(~cellfun(@isempty, indexes));

%% load masks
clear mask
for in = 1:3
    filename = [temp_path '\' filelist(indexes_bet(in)).name]
 %   mask(in) = load_nii(filename, [], [], [], [], [] , 1, []);
    mask(in) = load_untouch_nii(filename);
    mask(in).img = double(mask(in).img);  %% typecast added 22/1/2020
end

% combine masks 1:3 (white matter, grey matter and CSF) to build a brain
% mask
brain_mask = double(mask(1).img + mask(2).img + mask(3).img);

brain_mask = brain_mask/max(brain_mask(:));
brain_mask(brain_mask>0) = 1;
se = ones(3,3,3);
brain_mask = imclose(brain_mask,se);
gaussKernel = fast_3D_Gaussian([1 1 1],[3 3 3]);
brain_mask = imfilter(brain_mask, gaussKernel);

for in = 1:5
    filename = [temp_path '\' filelist(indexes_bet(in)).name]
 	delete(filename);
end



clear nii

    nii = load_untouch_nii(input_file);
    nii.img(isnan(nii.img)) = 0;            

        
nii_bet = nii;
         
    nii_bet.img = double(nii.img) .* brain_mask;
    nii_bet.img = uint16(nii_bet.img);
 
    pixel_sizes = nii.hdr.dime.pixdim(2:4);
    offsets = (size(nii.img))/2; % Nifti offset of the Anterior comissure. It´s in pixels, not mm!! 
    new_nii = make_nii(nii_bet.img, permute(pixel_sizes, [2 1 3]), permute(offsets, [2 1 3]), 4)

    
% Write masked images

slashes = strfind(input_file,'\');


     output_file = [input_file(1:slashes(end)) 'bet_' input_file(slashes(end)+1:end)]
     %save_untouch_nii(nii_bet, output_file)
     save_nii(new_nii, output_file)


delete([temp_path '\*.mat']);