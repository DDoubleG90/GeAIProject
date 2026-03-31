import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            
        # Will be True or False
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file])

        # Checking if the target dir is within working directory
        if valid_target_file_path != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Checking if the directory argument is not a directory,
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" is not a file'
        
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    
    except Exception as e:
        print(f"Error encountered: {e}")
