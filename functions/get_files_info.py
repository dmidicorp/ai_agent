import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        wd_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_path, directory))
        valid_target_dir = os.path.commonpath([wd_path, target_dir]) == wd_path

        if os.path.isdir(target_dir) == False:
            print(f'Error: "{directory}" is not a directory')
        elif valid_target_dir == False:
            print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        else:
            print(f'Success: "{directory}" is within the working directory')
    except Exception as e:
        print(f"Error: {e}")

    if valid_target_dir == True:
        files_in_dir = os.listdir(target_dir)

        dir_content = ""

        for file in files_in_dir:
            size = os.path.getsize(f"{target_dir}/{file}")
            is_dir = f"{os.path.isdir(os.path.join(wd_path, file))}\n"
            dir_content = dir_content + f"  - {file}: file_size={size} is_dir={is_dir}"
        if directory == ".":
            print(f"Result for current directory:")
        else:
            print(f"Result for {directory} directory:")
        print(dir_content)
