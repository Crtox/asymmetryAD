function out_dir = make_nii_single_file(input_dir, out_dir);
%% Converts all the Nifti files in input_dir to single files (.nii instead of .hdr + .img)

file_list = dir(input_dir)
filenames = {file_list.name}
file_indexes = strfind(filenames,'.img');


ii = 1;
for i = 1:length(file_indexes)
    index = cell2mat(file_indexes(i));
    if(isempty(index))
    else
    fname = cell2mat(filenames(i))
    full_file_name = [input_dir fname]  
    nii = load_nii(full_file_name);
  %  nii.untouch = 0;
    nii.hdr.dime.datatype = 16;  %% typecast added 22/1/2020
    nii.hdr.dime.bitpix = 16;   %% typecast added 22/1/2020
    nii.img = double(nii.img);  %% typecast added 22/1/2020
    
    out_filename = [out_dir '\' fname(1:end-3) 'nii'];
     save_nii(nii, out_filename)
    end
end
    
