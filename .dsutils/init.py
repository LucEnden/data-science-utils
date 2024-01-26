from internals import *
import os, sys


def __main__():
    """
    - Creates a .dsutils.env file in the project root directory
    - Asks the user what the root directory is of the project they want use DSUtils with
    - Writes the following to the .dsutils.env file:
        - PROJECT_ROOT=<project_root_directory>
    """
    #region Cleanup
    def __cleanup__():
        if os.path.isfile(ENV_FILE):
            os.remove(ENV_FILE)
        sys.exit(1)

    #region Environment file creation
    try:
        if os.path.isfile(ENV_FILE):
            dsutils_warn("Environment file already exists. Continuing will overwrite the existing environment file.")
            awnser = dsutils_input("Continue? (y/n): ")

            while True:
                if awnser == "y":
                    break
                elif awnser == "n":
                    dsutils_info("Exiting...")
                    sys.exit(0)
                else:
                    dsutils_warn("Please enter either 'y' or 'n'")
                    awnser = dsutils_input("Continue? (y/n): ")

        with open(ENV_FILE, "w") as f:
            f.write("")

        dsutils_success(f"Created DSUtils environment file: {ENV_FILE}")
    except KeyboardInterrupt:
        dsutils_error("KeyboardInterrupt")
        __cleanup__()
        sys.exit(1)
    #endregion

    #region Project root directory
    PROJECT_ROOT = None
    try:
        def __ask_user_to_set_project_root__():
            # Ask the user what the root directory is of the project they want to use DSUtils with
            awnser = dsutils_input("Please enter the root directory of your project: ")

            # Parse the input
            awnser = awnser.strip()
            awnser = os.path.abspath(awnser)

            return awnser


        PROJECT_ROOT = __ask_user_to_set_project_root__()
        is_root_correct = "n"
        root_is_correct = False
        
        while not root_is_correct:
            dsutils_info(f"Is this correct: {PROJECT_ROOT}")
            is_root_correct = dsutils_input(f"(y/n): ")
            if is_root_correct == "y":
                root_is_correct = True
            elif is_root_correct == "n":
                PROJECT_ROOT = __ask_user_to_set_project_root__()
            else:
                dsutils_warn("Please enter either 'y' or 'n'")

        with open(ENV_FILE, "a") as f:
            f.write(f"PROJECT_ROOT={PROJECT_ROOT}")

        dsutils_success(f"Set PROJECT_ROOT to: {PROJECT_ROOT}")

    except KeyboardInterrupt:
        dsutils_error("KeyboardInterrupt")
        __cleanup__()
        sys.exit(1)
    #endregion



if __name__ == "__main__":
    __main__()