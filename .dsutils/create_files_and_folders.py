from internals import *
import os
import json


def __get_files_and_folders__():
    """
    Returns a dictionary of the files and folders that need to be created.

    The dictionary has the following structure:
    ```json
    {
        "file_or_folder": {
            "path": "<path to file or folder>",
            "isFile": "<true if file false if folder>",
            "fileContents": "<contents of file, either as string or list. empty string if content is not applicable.>"
        },
    }
    """
    with open(os.path.join(os.path.dirname(__file__), "files_and_folders.json"), "r") as file:
        files_and_folders = json.load(file)

    project_root = dsutils_get_project_root()
    for f in files_and_folders:
        # Add the project root to the path
        files_and_folders[f]["path"] = project_root + files_and_folders[f]["path"]
        # Parse the file contents
        if bool(files_and_folders[f]['isFile']):
            if isinstance(files_and_folders[f]['fileContents'], list):
                files_and_folders[f]['fileContents'] = "\n".join(files_and_folders[f]['fileContents'])


    return files_and_folders


def __cleanup__():
    """
    Removes all files and folders that were created by this script.
    """
    files_and_folders = __get_files_and_folders__()

    for f in files_and_folders:
        if os.path.isfile(files_and_folders[f]["path"]):
            os.remove(files_and_folders[f]["path"])
        elif os.path.isdir(files_and_folders[f]["path"]):
            os.rmdir(files_and_folders[f]["path"])


def __create_files_and_folders__():
    """
    Creates files and folders to house the data, artefacts and experiments of the project.

    If any of the files or folders already exist, a warning is printed to the console.

    The following files and folders are created:
    ```plaintext
    <project_root>
    |
    +--/ artefacts
    |  | artefacts.py
    |
    +--/ data
    |  +--- processed
    |  +--- raw
    |
    +--/ experiments
    ```
    """

    try:
        files_and_folders = __get_files_and_folders__()

        dsutils_info("Creating files and folders...")
        for f in files_and_folders:
            if os.path.isfile(files_and_folders[f]['path']) or os.path.isdir(files_and_folders[f]['path']):
                dsutils_warn(f"\t{files_and_folders[f]["path"]} (already exists)")
            else:
                if bool(files_and_folders[f]['isFile']):
                    if isinstance(files_and_folders[f]['fileContents'], list):
                        files_and_folders[f]['fileContents'] = "\n".join(files_and_folders[f]['fileContents'])

                    with open(files_and_folders[f]['path'], "w") as file:
                        file.write(files_and_folders[f]['fileContents'])
                else:
                    os.mkdir(files_and_folders[f]['path'])
                dsutils_success(f"\t{files_and_folders[f]['path']}")
    except KeyboardInterrupt:
        dsutils_error("KeyboardInterrupt")
        __cleanup__()
        sys.exit(1)
    except Exception as e:
        dsutils_error(e)
        __cleanup__()
        sys.exit(1)


def __main__():
    """
    Creates the files and folders needed to house the data, artefacts and experiments of the project.

    The main function is called when the script is run from the command line.
    The create_files_and_folders function was separated from the main function to allow for the creation of the files and folders from other scripts.
    """
    __create_files_and_folders__()


if __name__ == "__main__":
    __main__()