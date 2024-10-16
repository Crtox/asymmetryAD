input_dir = 'G:\MATLAB\R2013a\work\QTNI\temp\';  % Directory containing all original nifti files
output_dir = 'G:\MATLAB\R2013a\work\QTNI\Fixed\';

files = dir(input_dir);

progressbar()
for i = 3:length(files)  
    input_file = [input_dir '\' files(i).name];
    nii = load_nii(input_file);
    
    nii.original.hdr.dime
    
    pixel_sizes = nii.original.hdr.dime.pixdim(2:4);
    offsets = (size(nii.img))/2; % Nifti offset of the Anterior comissure. It´s in pixels, not mm!! 
    
    new_nii = make_nii(nii.img, permute(pixel_sizes, [2 1 3]), permute(offsets, [2 1 3]), 16, files(i).name)
    save_nii(new_nii, [output_dir '\' files(i).name]) 
    
    progressbar(i/(length(files)-3));
end