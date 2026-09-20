import os
import subprocess


schema_run_python_file = {
        "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Executes a given python file provided in file_path, using the args as arguments",
            "parameters": {
                "required": ["file_path"],
                "type": "object",
                "file_path": {
                    "type": "string",
                    "description": "A valid python executable file, with a .py extension that should be executed with ars as its arguments passed into it",
                    },
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "List of arguments passed into the python executable file by the function"
                }
            }
        }
    }


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    wd_path = os.path.normpath(os.path.abspath((working_directory)))
    target_file = os.path.normpath(os.path.join(wd_path, file_path))
    is_valid_dir = os.path.commonpath([wd_path, target_file]) == wd_path

    if is_valid_dir == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


    if os.path.isfile(target_file) == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if target_file.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args:
        command.extend(args)

    try:
        process = subprocess.run(command, cwd=wd_path, timeout=30, capture_output=True, text=True, check=True)
        output_string = ""
    
        if process:
            if process.returncode != 0:
                output_string += f'"Process exited with code: {process.returncode}'

            if not process.stdout and not process.stderr:
                output_string += '"No output produced" '

            if process.stdout:
                output_string += f"STDOUT: {process.stdout}"
            
            if process.stderr:
                output_string += f"STDERR: {process.stderr}"
            else:
                no_output = 'STDERR: "No output produced"'
                output_string += no_output
                

            return output_string

                    
            
    except Exception as e:
        return f'Error: executing Python file: {e}'
                            



