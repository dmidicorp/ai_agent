import os


schema_write_file = {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content into a specified file, or overwrites file content, relative to the working directory, and also creates any missing parent directories",
            "parameters": {
                "required": ["file_path", "content"], 
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File to write content into. Must contain valid path relative to the working directory",
                        },
                    "content": {
                        "type": "string",
                        "description": "content to be written to file defined in file_path"
                    }
                }
            } 
        }
    }



def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        wd_path = os.path.normpath(os.path.abspath(working_directory)) 
        target_file = os.path.normpath(os.path.join(wd_path, file_path))
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_file)

        is_valid_dir = os.path.commonpath([wd_path, parent_dir, target_file]) == wd_path
        if is_valid_dir == False:
            return f'Error: Cannot read/write "{file_path}" as it is outside the permitted working directory'

        try:
            os.makedirs(parent_dir, mode=0o777, exist_ok=True)

            if os.path.isdir(parent_dir):
                with open(target_file, "w") as f:
                    f.write(content)
                    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
        except Exception as e:
            return f"Error: failed to create directory. {e}"


    except Exception as e:
        if e != None:
            return f"Error: {e}"
        else: 
            return f"Error: unknown exception error: {e}"

