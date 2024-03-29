# Add the dsutils directory to the path so that we can import from it when running this file directly
import os, sys
if __name__ == "__main__":
    dsutils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, dsutils_path)

from dsutils.internals import *
from dsutils.create_files_and_folders import create_files_and_folders, __get_files_and_folders_from_json__, __remove_files_and_folders__
import argparse


PROJECT_ROOT = None
CREATED_FILES_AND_FOLDERS_CALLED = False

DSUTILS_START = """
#===========================================================#
#                                                           #
#   Welcome to DSUtils!                                     #
#                                                           #
#   This setup will guide you through the process of        #
#   setting up DSUtils for your project.                    #
#                                                           #
#===========================================================#
"""
DSUTILS_FINISHED = """
#===========================================================#
#                                                           #
#   Setup completed successfully!                           #
#   Happy coding!                                           #
#                                                           #
#===========================================================#
"""


def __cleanup__():
    global CREATED_FILES_AND_FOLDERS_CALLED

    try:
        if os.path.isfile(ENV_FILE):
            os.remove(ENV_FILE)
        if CREATED_FILES_AND_FOLDERS_CALLED:
            __remove_files_and_folders__()
    except Exception as e:
        dsutils_error("Exception occured while cleaning up:")
        dsutils_error(e)


def setup():
    """
    Creates the .dsutils.env file in the project root directory
    
    It then asks the user what the root directory is of the project they want use DSUtils with. The awnser is then written to the .dsutils.env file.

    It then creates the files and folders needed to house the data, artifacts and experiments of the project.
    """
    global PROJECT_ROOT, CREATED_FILES_AND_FOLDERS_CALLED

    parser = argparse.ArgumentParser(description='Initialize DSUtils for the given project.')
    parser.add_argument('-p', '--projectroot', default=None, help='The path (relative or absolute) to the root directory of the project you want to use DSUtils with.')
    args = parser.parse_args()
    PROJECT_ROOT = args.projectroot

    dsutils_info(DSUTILS_START)

    try:
        #region Parse project root directory
        if PROJECT_ROOT is None:
            # Ask the user what the root directory is of the project they want to use DSUtils with
            PROJECT_ROOT = dsutils_input("Please enter the root directory of your project: ")
            PROJECT_ROOT = os.path.abspath(PROJECT_ROOT.strip())
        else:
            PROJECT_ROOT = os.path.abspath(str(PROJECT_ROOT).strip())

        is_root_correct = "n"
        root_is_correct = False
        
        while not root_is_correct:
            dsutils_info(f"Is this the path to the root directory of your project?")
            dsutils_info(f"{PROJECT_ROOT}")
            is_root_correct = dsutils_input_yes_no(f"(y/n): ")
            if is_root_correct:
                root_is_correct = True
            else:
                PROJECT_ROOT = dsutils_input("Please enter the root directory of your project: ")
                PROJECT_ROOT = os.path.abspath(PROJECT_ROOT.strip())

        dsutils_success(f"PROJECT_ROOT was set to: {PROJECT_ROOT}")
        #endregion

        #region Verify environment file does not exist, or ask user if they want to overwrite it
        env_file_path = PROJECT_ROOT + ENV_FILE.replace("/", os.sep)
        if os.path.isfile(env_file_path):
            dsutils_warn("Environment file for DSUtils already exists.")
            dsutils_warn("This probably means that DSUtils has already been setup for this project.")
            dsutils_warn("Continuing will overwrite the existing environment file.")
            awnser = dsutils_input_yes_no("Continue? (y/n): ")
            dsutils_warn(awnser)

            if not awnser:
                dsutils_warn("Not overwriting environment file.")
                dsutils_warn("Exiting setup.")
                sys.exit(0)
            else:
                dsutils_warn("Overwriting environment file.")
                os.remove(env_file_path)
        #endregion
                
        #region Create files and folders
        created_paths = create_files_and_folders(PROJECT_ROOT)
        CREATED_FILES_AND_FOLDERS_CALLED = True
        #endregion

        #region Create environment file
        env_vars = [
            ("PROJECT_ROOT", PROJECT_ROOT),
            ("PROJECT_NAME", os.path.basename(PROJECT_ROOT))
        ]
        for key, value in zip(__get_files_and_folders_from_json__(PROJECT_ROOT), created_paths):
            if key != "env_file":
                env_vars.append((str(key).upper(), value.replace(PROJECT_ROOT, "")))

        with open(env_file_path, "w") as f:
            for i, v in enumerate(env_vars):
                f.write(f"{v[0]}={v[1]}")
                if i < len(env_vars) - 1:
                    f.write("\n")

        dsutils_success(f"Created DSUtils environment file at: {env_file_path}")
        #endregion

        # TODO: Update gitignore

        dsutils_success(DSUTILS_FINISHED)
            
    except KeyboardInterrupt:
        dsutils_error("KeyboardInterrupt")
        __cleanup__()
        sys.exit(1)


if __name__ == "__main__":
    setup()