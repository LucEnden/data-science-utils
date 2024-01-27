import os
import sys
from datetime import datetime


ENV_FILE = "/.dsutils.env"
SOURCES_FILE = "/sources.csv"
ARTIFACTS_DIR = "/artefacts"
DATA_DIR = "/data"
PROCESSED_DIR = DATA_DIR + "/processed"
RAW_DIR = DATA_DIR + "/raw"


#region Console Methods
class LogOptions:
    clr_WHITE = '\033[97m'
    clr_PURPLE = '\033[95m'
    clr_BLUE = '\033[94m'
    clr_CYAN = '\033[96m'
    clr_GREEN = '\033[92m'
    clr_YELLOW = '\033[93m'
    clr_RED = '\033[91m'
    clr_ENDC = '\033[0m'
    trs_BOLD = '\033[1m'
    trs_UNDERLINE = '\033[4m'
    END = '\033[0m'


def __parse_logoptions__(log_options: list[LogOptions] = []):
    """
    Parses a list of LogOptions into a string.

    Args:
        log_options (list[LogOptions], optional): A list of LogOptions. Defaults to [].

    Returns:
        str: A string containing the LogOptions.
    """
    # If no log_options are provided, default to white
    if len(log_options) == 0:
        log_options = [ LogOptions.clr_WHITE ]

    # Remove END option if it exists
    if LogOptions.END in log_options:
        log_options.remove(LogOptions.END)

    join_options = "".join(log_options)
    return join_options


def __dfutils_log__(message: str, log_options: list[LogOptions] = []):
    """
    Logs a message with the specified formatting log_options.

    Args:
        message (str): The message to log.
        log_options (list[LogOptions], optional): A list of formatting log_options. Defaults to [].
    """
    print(f"{__parse_logoptions__(log_options)}[DSUTILS | {datetime.now().strftime('%H:%M:%S')}]:{LogOptions.END} {message}")


def dsutils_info(message: str):
    """
    Logs a message with plain white text.

    Args:
        message (str): The message to log.
    """
    __dfutils_log__(message, [ LogOptions.clr_WHITE ])


def dsutils_success(message: str):
    """
    Logs a success message with green, bold, and underlined text.

    Args:
        message (str): The message to log.
    """
    __dfutils_log__(message, [ LogOptions.clr_GREEN, LogOptions.trs_BOLD, LogOptions.trs_UNDERLINE ])


def dsutils_warn(message: str):
    """
    Logs a warning message with yellow, bold, and underlined text.

    Args:
        message (str): The message to log.
    """
    __dfutils_log__(message, [ LogOptions.clr_YELLOW, LogOptions.trs_BOLD, LogOptions.trs_UNDERLINE ])
    

def dsutils_error(message: str):
    """
    Logs an error message with red, bold, and underlined text.

    Args:
        message (str): The message to log.
    """
    __dfutils_log__(message, [ LogOptions.clr_RED, LogOptions.trs_BOLD, LogOptions.trs_UNDERLINE ])
#endregion
    

#region Input Methods
def dsutils_input(message: str, log_options: list[LogOptions] = []):
    """
    Prompts the user for input with a formatted message.

    Args:
        message (str): The message to display.
        log_options (list[LogOptions], optional): A list of formatting log_options. Defaults to [].

    Returns:
        str: The user's input.
    """
    return input(f"{__parse_logoptions__(log_options)}[DSUTILS | {datetime.now().strftime('%H:%M:%S')}]:{LogOptions.END} {message}")


def dsutils_input_options(message: str, options: list[str], log_options: list[LogOptions] = []):
    """
    Prompts the user for input with a formatted message and a list of options.

    Args:
        message (str): The message to display.
        options (list[str]): A list of options to display.
        log_options (list[LogOptions], optional): A list of formatting log_options. Defaults to [].

    Returns:
        str: The selected option.
    """
    dsutils_info(f"{message}")

    indexed_options = [ (i + 1, o) for i, o in enumerate(options)]
    max_index_length = len(str(len(indexed_options)))
    for i in indexed_options:
        # Print the options with a number in front of them and the right indentation
        ind = i[0]
        opt = i[1]
        spaces = " " * (max_index_length - len(str(ind)))

        dsutils_info(f"{ind}{spaces} > {opt}")

    awnser = dsutils_input(message, log_options)
    while True:
        if awnser in [ str(i[0]) for i in indexed_options ]:
            return options[int(awnser) - 1]
        elif awnser in [ i[1] for i in indexed_options ]:
            return awnser
        else:
            dsutils_warn(f"Please enter one of the options above, either the number or the option itself.")
            awnser = dsutils_input(message, log_options)


def dsutils_input_yes_no(message: str, log_options: list[LogOptions] = []):
    """
    Prompts the user for a yes or no response.

    Args:
        message (str): The message to display.
        log_options (list[LogOptions], optional): A list of formatting log_options. Defaults to [].

    Returns:
        bool: True if the user responds with 'y', False if the user responds with 'n'.
    """
    awnser = dsutils_input(message, log_options)
    while True:
        if awnser == "y":
            return True
        elif awnser == "n":
            return False
        else:
            dsutils_warn("Please enter 'y' or 'n'")
            awnser = dsutils_input(message, log_options)
#endregion


def dsutils_read_env(project_root: str = os.getcwd()):
    """
    Reads the environment file and returns a dictionary of the environment variables.

    If the environment file does not exist, an error is printed to the console and the program exits.

    Args:
        project_root (str, optional): The root directory of the project. Defaults to `os.getcwd()`.

    Returns:
        dict: A dictionary of the environment variables.
    """
    ENV_FILE = os.path.join(project_root, ENV_FILE)
    if not os.path.isfile(ENV_FILE):
        dsutils_error("Environment file does not exist.")
        dsutils_error("This probably means that DSUtils has not been initialized for this project.")
        dsutils_error("Please run the DSUtils initialization script before continuing.")
        dsutils_error("Exiting...")
        sys.exit(1)

    with open(ENV_FILE) as f:
        env_vars = f.read().splitlines()
        env_dict = {}
        for v in env_vars:
            env_dict[v.split("=")[0]] = v.split("=")[1]

    return env_dict


def dsutils_get_project_root():
    """
    Returns the root directory of the project.

    Returns:
        str: The root directory of the project.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    return project_root


def dsutils_get_project_name():
    """
    Returns the name of the project.

    Returns:
        str: The name of the project.
    """
    envs = dsutils_read_env()
    project_name = envs["PROJECT_NAME"]
    return project_name


def dsutils_get_sources_file_content():
    """
    Reads the sources file and returns a list of the lines.

    If the sources file does not exist, an error is printed to the console and the program exits.
    """
    envs = dsutils_read_env()
    SOURCES_FILE = envs["SOURCES_FILE"]

    if not os.path.isfile(SOURCES_FILE):
        dsutils_error(f"Sources file does not exist: {SOURCES_FILE}")
        dsutils_error("This probably means that DSUtils has not been initialized for this project.")
        dsutils_error("Please run the DSUtils initialization script before continuing.")
        dsutils_error("Exiting...")
        sys.exit(1)

    with open(SOURCES_FILE, 'r') as file:
        sources = file.readlines()
        return sources