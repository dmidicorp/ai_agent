import os

schema_get_files_info = {
        "type": "function",
        "function": {
            "name": "get_files_info", 
            "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string", 
                        "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                        }
                    }
                }
            }
        }


def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        wd_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_path, directory))
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
        
        valid_target_dir = os.path.commonpath([wd_path, target_dir]) == wd_path
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

    dir_content = ""
    files_in_dir = os.listdir(target_dir)


    for file in files_in_dir:
        size = os.path.getsize(f"{target_dir}/{file}")
        is_dir = f"{os.path.isdir(os.path.join(wd_path, file))}\n"
        dir_content = dir_content + f"  - {file}: file_size={size} is_dir={is_dir}"
    if directory == ".":
        return f"Result for current directory:\n{dir_content}"
    else:
        return f"Result for {directory} directory:\n{dir_content}"
