import os
from constants import MAX_CHARS

schema_get_file_content = {
        "type": "function", 
        "function": {
            "name": "get_file_content",
            "description": "Lists the file content of a given file inside file_path, truncates output of long text files at 10000 characters",
            "parameters": {
                "required": ["file_path"],
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File to read the content from, must be a valid file, relative to the working directory"
                        }
                    }
                }
            }
        }


def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        wd_path = os.path.normpath(os.path.abspath(working_directory)) 
        target_file = os.path.normpath(os.path.join(wd_path, file_path))

        is_valid_dir = os.path.commonpath([wd_path, target_file]) == wd_path
        if is_valid_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        is_valid_file = os.path.isfile(target_file)
        if is_valid_file == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
       
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return file_content_string

    except Exception as e:
        return f"Error: {e}"


