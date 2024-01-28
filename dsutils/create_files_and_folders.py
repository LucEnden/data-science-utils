# Add the dsutils directory to the path so that we can import from it when running this file directly
import os, sys
if __name__ == "__main__":
    dsutils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, dsutils_path)

from dsutils.internals import *
import json


def __get_files_and_folders_from_json__(project_root: str | None = None):
    """
    Returns a dictionary of the files and folders that need to be created.

    The dictionary has the following structure:
    ```json
    {
        "file_or_folder": {
            "path": "<path to file or folder>",
            "isFile": "<true if file, false if folder>",
            "fileContents": "<contents of file, either as string or list. empty string if file content is not applicable>"
        },
        ...
    }
    """
    if project_root is None:
        project_root = dsutils_get_project_root()

    with open(os.path.join(os.path.dirname(__file__), "files_and_folders.json"), "r") as file:
        files_and_folders = json.load(file)

    for f in files_and_folders:
        # Add the project root to the path
        files_and_folders[f]["path"] = project_root + str(files_and_folders[f]["path"]).replace("/", os.sep)
        # Parse the file contents
        if bool(files_and_folders[f]['isFile']):
            # We assume that the file contents are a list of strings or a string
            # A test case for this is in tests/create_files_and_folders_test.py
            # As such, we need to convert the list to a string
            if isinstance(files_and_folders[f]['fileContents'], list):
                files_and_folders[f]['fileContents'] = "\n".join(files_and_folders[f]['fileContents'])

    return files_and_folders


def __remove_files_and_folders__(project_root: str | None = None):
    """
    Removes all files and folders that were created by this script, if any.

    If an error occurs while removing a file or folder, the error is printed to the console and the file or folder is not removed.

    Warning
    -------
    This function is not meant to be called by the user. It is only meant to be called by the `__main__` function of this script or in the `dsutils/setup.py` file.
    Use at your own risk.
    """

    if project_root is None:
        project_root = dsutils_get_project_root()
    elif not os.path.exists(project_root) or not os.path.isdir(project_root):
        dsutils_error(f"Project root does not exist or is not a directory: {project_root}")
        dsutils_error("Please enter a valid project root.")
        dsutils_error("Aborting...")
        sys.exit(1)

    files_and_folders = __get_files_and_folders_from_json__(project_root)
    # Sort the files and folders such that:
    # 1. Files are removed before folders
    # 2. Files and folders are removed from the deepest path to the shallowest path
    # Deepest meaning the path with the most subdirectories, i.e. path with the most os.sep
    files_and_folders = {
        k: v for k, v in sorted(files_and_folders.items(), key=lambda item: (not item[1]["isFile"], item[1]["path"].count(os.sep)), reverse=True)
    }

    dsutils_warn("Removing files and folders...")
    for f in files_and_folders:
        try:
            if os.path.isfile(files_and_folders[f]["path"]):
                os.remove(files_and_folders[f]["path"])
            elif os.path.isdir(files_and_folders[f]["path"]):
                os.rmdir(files_and_folders[f]["path"])
        except Exception as e:
            dsutils_error(f"Failed to remove {files_and_folders[f]['path']}")
            dsutils_error(e)


def create_files_and_folders(project_root: str | None = None):
    """
    Creates the files and folders provided by DSUtils. For more information on the files and folders, see the `files_and_folders.json` file.

    If a file or folder already exists, it is not overwritten.

    Args:
    -----
        project_root (str, optional): The root directory of the project. Defaults to `dsutils_get_project_root()`.

    Returns:
    --------
        list[str]: A list of the paths to the files and folders that were created.
    """
    if project_root is None:
        project_root = dsutils_get_project_root()

    files_and_folders = __get_files_and_folders_from_json__(project_root)
    paths: list[str] = []

    try:
        dsutils_info("Creating files and folders...")
        for f in files_and_folders:
            if os.path.isfile(files_and_folders[f]['path']) or os.path.isdir(files_and_folders[f]['path']):
                dsutils_warn(f"\t{files_and_folders[f]['path']} (already exists)")
            else:
                if bool(files_and_folders[f]['isFile']):
                    if isinstance(files_and_folders[f]['fileContents'], list):
                        files_and_folders[f]['fileContents'] = "\n".join(files_and_folders[f]['fileContents'])

                    with open(files_and_folders[f]['path'], "w") as file:
                        file.write(files_and_folders[f]['fileContents'])
                else:
                    os.mkdir(files_and_folders[f]['path'])
                dsutils_success(f"\t{files_and_folders[f]['path']}")

            paths.append(str(files_and_folders[f]['path']))

        return paths
    except KeyboardInterrupt:
        dsutils_error("KeyboardInterrupt")
        __remove_files_and_folders__()
        sys.exit(1)
    except Exception as e:
        dsutils_error(e)
        __remove_files_and_folders__()
        sys.exit(1)


if __name__ == "__main__":
    create_files_and_folders()