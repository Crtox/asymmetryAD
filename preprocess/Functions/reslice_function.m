function output_file = reslice_function(input_file, options)

temp_path = options.temp_path;

slashes = strfind(input_file,'\');
output_file = [temp_path 'rsl_' input_file(slashes(end)+1:end)]


reslice_nii(input_file, output_file, [2 2 2]);