function output_file = fix_nifti_coords_function(input_file, options);


nii = load_nii(input_file);
%nii = load_untouch_nii(input_file);
%nii.original.hdr.dime
    
%pixel_sizes = nii.original.hdr.dime.pixdim(2:4);
pixel_sizes = nii.hdr.dime.pixdim(2:4);

zp = squeeze(sum(sum(nii.img,1),2));
nii.img(:,:,zp==0) = [];
%mask = nii.img > 2;
%stats = regionprops(mask);
%pepe = stats.Centroid;
%offsets = round(pepe);
offsets = (size(nii.img))/2; % Nifti offset of the Anterior comissure. It´s in pixels, not mm!! 
    

slashes = strfind(input_file,'\');
nombre = input_file(slashes(end)+1:end);
new_nii = make_nii(nii.img, permute(pixel_sizes, [2 1 3]), permute(offsets, [2 1 3]), 4, nombre);

output_file =  [options.temp_path 'f_' nombre];
save_nii(new_nii, output_file) 
    

