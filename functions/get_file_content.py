import os
from constants import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        wd_path = os.path.normpath(os.path.abspath(working_directory)) 
        target_file = os.path.normpath(os.path.join(wd_path, file_path))
        is_valid_dir = os.path.commonpath([wd_path, target_file]) == wd_path
        is_valid_file = os.path.isfile(target_file)

        if is_valid_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif is_valid_file == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
       
        if is_valid_file and is_valid_dir:
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            if file_content_string:
                return file_content_string
    except Exception as e:
        if e != None:
            print(f"Error: {e}")


