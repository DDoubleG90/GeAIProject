import os
import config

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir_file])


    # Checking if the target file is within working directory
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Checking if the file is a directory,
    if os.path.isdir(target_dir_file) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    parent_dir = os.path.dirname(target_dir_file)

    os.makedirs(parent_dir, exist_ok=True)

    with open(target_dir_file, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
