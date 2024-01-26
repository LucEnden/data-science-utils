from internals import *
from create_files_and_folders import __create_files_and_folders__, __cleanup__ as __cleanup_create_files_and_folders__
import os, sys
import argparse


parser = argparse.ArgumentParser(description='Initialize DSUtils for the given project.')
parser.add_argument('-p', '--projectroot', default=None, help='The path (relative or absolute) to the root directory of the project you want to use DSUtils with.')
args = parser.parse_args()
PROJECT_ROOT = args.projectroot


def __cleanup__():
    if os.path.isfile(ENV_FILE):
        os.remove(ENV_FILE)
    __cleanup_create_files_and_folders__()
    sys.exit(1)


def __main__():
    """
    Creates the .dsutils.env file in the project root directory
    
    It then asks the user what the root directory is of the project they want use DSUtils with. The awnser is then written to the .dsutils.env file.

    It then creates the files and folders needed to house the data, artefacts and experiments of the project.
    """
    global PROJECT_ROOT

    try:
        #region Verify environment file does not exist, or ask user if they want to overwrite it
        if os.path.isfile(ENV_FILE):
            dsutils_warn("Environment file already exists. This probably means that DSUtils has already been initialized for this project.")
            dsutils_warn("Continuing will overwrite the existing environment file.")
            awnser = dsutils_yes_no("Continue? (y/n): ")

            if not awnser:
                dsutils_info("Exiting...")
                sys.exit(0)
            else:
                os.remove(ENV_FILE)
        #endregion

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
            dsutils_info(f"\t{PROJECT_ROOT}")
            is_root_correct = dsutils_input(f"(y/n): ")
            if is_root_correct == "y":
                root_is_correct = True
            elif is_root_correct == "n":
                PROJECT_ROOT = dsutils_input("Please enter the root directory of your project: ")
                PROJECT_ROOT = os.path.abspath(PROJECT_ROOT.strip())
            else:
                dsutils_warn("Please enter either 'y' or 'n'")

        with open(ENV_FILE, "a") as f:
            f.write(f"PROJECT_ROOT={PROJECT_ROOT}")

        dsutils_success(f"Set PROJECT_ROOT to: {PROJECT_ROOT}")
        #endregion
            
        #region Create files and folders
        __create_files_and_folders__()
        #endregion

        #region Create environment file
        with open(ENV_FILE, "w") as f:
            f.write("")

        dsutils_success(f"Created DSUtils environment file: {ENV_FILE}")
        #endregion
    except KeyboardInterrupt:
        dsutils_error("KeyboardInterrupt")
        __cleanup__()
        sys.exit(1)


if __name__ == "__main__":
    __main__()