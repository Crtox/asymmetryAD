function output_file = GM_intensity_normalization(input_file, options)
% function normalized = intensity_normalization(input_file, options)
% Normalizes the intensity to the template (Global mean)
% v1.0 - December 10 2019
% Mauro Namías - mauro.namias@gmail.com

temp_path = options.temp_path;

% Load files
ref = options.PET_template;
template = load_nii(ref)
at = options.PET_atlas;
atlas = load_nii(at);

nii = load_nii(input_file)
nii_filtered = nii;
pixel_sizes = [2 2 2];
TF = isinteger(nii.img)
    
nii_filtered.img = filtra_3D(nii.img, pixel_sizes, [8 8 8]);
mask = atlas.img > 0;

dat(:,1) = template.img(mask == 1);
dat(:,2) = nii_filtered.img(mask == 1);             

GMs = mean(dat,1);

factor = GMs(1)/GMs(2); 

%% apply factors
nii.img = nii.img * double(factor);
         
% Write unbiased image
slashes = strfind(input_file,'\');
output_file = [input_file(1:slashes(end)) 'GM_' input_file(slashes(end)+1:end)];
save_nii(nii, output_file);



    