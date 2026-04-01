import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_dir_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir_file])

        # Checking if the target file is within working directory
        if valid_target_dir != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Checking if the file is a file,
        if os.path.isfile(target_dir_file) == True:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # Checking if the file is a python file,
        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'
        
        # Commands List
        command = ["python", target_dir_file]
        if args != None:
            command.extend(args)
        
        # Running subprocess
        completed_process_object = subprocess.run(command, cwd=working_dir_abs, capture_output=True,text=True,timeout=30)
        output_string = ""
        if completed_process_object.returncode != 0:
            output_string = f"Process exited with code{completed_process_object.returncode}"
        if completed_process_object.stdout == None and completed_process_object.stderr == None:
            output_string += "\nNo output produced"
        else:
            output_string += f"\nSTDOUT: {completed_process_object.stdout}\nSTDERR: {completed_process_object.stderr}"
        
        return output_string
    
    except Exception as e:
        print(f"Error: executing Python file: {e}")





