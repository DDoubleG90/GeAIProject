import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        
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
        
    except Exception as e:
        print(f"Error encountered: {e}")
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file the content specified by the user",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the specified file the user wants to write its content",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content the user wants to see written to the specified file",
            ),
        },
        required =["file_path", "content"]
    ),
)