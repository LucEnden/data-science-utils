import os
import sys
from datetime import datetime


ENV_FILE = "/.dsutils.env"


#region Console Methods
class __LogOptions__:
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


def __parse_logoptions__(log_options: list[__LogOptions__] = []):
    """
    Parses a list of __LogOptions__ into a string.

    Args:
    ------
        log_options (list[__LogOptions__], optional): A list of __LogOptions__. Defaults to [].

    Returns:
    ------
        str: A string containing the __LogOptions__.
    """
    # If no log_options are provided, default to white
    if len(log_options) == 0:
        log_options = [ __LogOptions__.clr_WHITE ]

    # Remove END option if it exists
    if __LogOptions__.END in log_options:
        log_options.remove(__LogOptions__.END)

    join_options = "".join(log_options)
    return join_options


def __dfutils_log__(message: str, log_options: list[__LogOptions__] = []):
    """
    Logs a message with the specified formatting log_options.

    Args:
    ------
        message (str): The message to log.
        log_options (list[__LogOptions__], optional): A list of formatting log_options. Defaults to [].
    """
    print(f"{__parse_logoptions__(log_options)}[DSUTILS | {datetime.now().strftime('%H:%M:%S')}]:{__LogOptions__.END} {message}")


def dsutils_info(message: str):
    """
    Logs a message with plain white text.

    Args:
    ------
        message (str): The message to log.
    """
    __dfutils_log__(message, [ __LogOptions__.clr_WHITE ])


def dsutils_success(message: str):
    """
    Logs a success message with green, bold, and underlined text.

    Args:
    ------
        message (str): The message to log.
    """
    __dfutils_log__(message, [ __LogOptions__.clr_GREEN, __LogOptions__.trs_BOLD, __LogOptions__.trs_UNDERLINE ])


def dsutils_warn(message: str):
    """
    Logs a warning message with yellow, bold, and underlined text.

    Args:
    ------
        message (str): The message to log.
    """
    __dfutils_log__(message, [ __LogOptions__.clr_YELLOW, __LogOptions__.trs_BOLD, __LogOptions__.trs_UNDERLINE ])
    

def dsutils_error(message: str):
    """
    Logs an error message with red, bold, and underlined text.

    Args:
    ------
        message (str): The message to log.
    """
    __dfutils_log__(message, [ __LogOptions__.clr_RED, __LogOptions__.trs_BOLD, __LogOptions__.trs_UNDERLINE ])
#endregion
    

#region Input Methods
def dsutils_input(message: str, log_options: list[__LogOptions__] = []):
    """
    Prompts the user for input with a formatted message.

    Args:
    ------
        message (str): The message to display.
        log_options (list[__LogOptions__], optional): A list of formatting log_options. Defaults to [].

    Returns:
    ------
        str: The user's input.
    """
    return input(f"{__parse_logoptions__(log_options)}[DSUTILS | {datetime.now().strftime('%H:%M:%S')}]:{__LogOptions__.END} {message}")


def dsutils_input_options(message: str, options: list[str], log_options: list[__LogOptions__] = []):
    """
    Prompts the user for input with a formatted message and a list of options.

    Args:
    ------
        message (str): The message to display.
        options (list[str]): A list of options to display.
        log_options (list[__LogOptions__], optional): A list of formatting log_options. Defaults to [].

    Returns:
    ------
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


def dsutils_input_yes_no(message: str, log_options: list[__LogOptions__] = []):
    """
    Prompts the user for a yes or no response.

    Args:
        message (str): The message to display.
        log_options (list[__LogOptions__], optional): A list of formatting log_options. Defaults to [].

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
    ------
        project_root (str, optional): The root directory of the project. Defaults to `os.getcwd()`.

    Returns:
    ------
        dict: A dictionary of the environment variables.
    """
    global ENV_FILE

    env = project_root + ENV_FILE.replace("/", os.sep)
    if not os.path.isfile(env):
        dsutils_error(f"Environment file does not exist:{env}")
        dsutils_error("This probably means that DSUtils has not been setup for this project.")
        dsutils_error("Please run the DSUtils setup script before continuing.")
        dsutils_error("Exiting...")
        sys.exit(1)

    with open(env) as f:
        env_vars = f.read().splitlines()
        env_dict: dict[str, str] = dict()
        for v in env_vars:
            env_dict[v.split("=")[0]] = v.split("=")[1]

    return env_dict


def dsutils_get_project_root():
    """
    Returns the root directory of the project.

    Equivalent to: `dsutils_read_env()["PROJECT_ROOT"]`.

    Returns:
    ------
        str: The root directory of the project.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    return str(project_root)


def dsutils_get_project_name():
    """
    Returns the name of the project.

    Equivalent to: `dsutils_read_env()["PROJECT_NAME"]`.

    Returns:
    ------
        str: The name of the project.
    """
    envs = dsutils_read_env()
    project_name = envs["PROJECT_NAME"]
    return str(project_name)


def dsutils_get_artifacts_dir():
    """
    Returns the path to the artifacts directory.

    Equivalent to: `dsutils_get_project_root() + dsutils_read_env()["ARTIFACTS_DIR"]`.

    Returns:
    ------
        str: The path to the artifacts directory.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    artifacts_dir = envs["ARTIFACTS_DIR"]
    return str(project_root) + str(artifacts_dir)


def dsutils_get_data_dir():
    """
    Returns the path to the data directory.

    Equivalent to: `dsutils_get_project_root() + dsutils_read_env()["DATA_DIR"]`.

    Returns:
    ------
        str: The path to the data directory.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    data_dir = envs["DATA_DIR"]
    return str(project_root) + str(data_dir)


def dsutils_get_data_processed_dir():
    """
    Returns the path to the processed data directory.

    Equivalent to: `dsutils_get_project_root() + dsutils_read_env()["DATA_PROCESSED_DIR"]`.

    Returns:
    ------
        str: The path to the processed data directory.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    processed_dir = envs["DATA_PROCESSED_DIR"]
    return str(project_root) + str(processed_dir)


def dsutils_get_data_raw_dir():
    """
    Returns the path to the raw data directory.

    Equivalent to: `dsutils_get_project_root() + dsutils_read_env()["DATA_RAW_DIR"]`.

    Returns:
    ------
        str: The path to the raw data directory.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    raw_dir = envs["DATA_RAW_DIR"]
    return str(project_root) + str(raw_dir)


def dsutils_get_experiments_dir():
    """
    Returns the path to the experiments directory.

    Equivalent to: `dsutils_get_project_root() + dsutils_read_env()["EXPERIMENTS_DIR"]`.

    Returns:
    ------
        str: The path to the experiments directory.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    experiments_dir = envs["EXPERIMENTS_DIR"]
    return str(project_root) + str(experiments_dir)


def dsutils_get_sources_file():
    """
    Returns the path to the sources file.

    Equivalent to: `dsutils_get_project_root() + dsutils_read_env()["SOURCES_FILE"]`.

    Returns:
    ------
        str: The path to the sources file.
    """
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]
    sources_file = envs["SOURCES_FILE"]
    return str(project_root) + str(sources_file)


def dsutils_get_sources_file_content():
    """
    Reads the sources file and returns a list of the lines.

    If the sources file does not exist, an error is printed to the console and the program exits.

    Returns:
    ------
        list: A list of the lines in the sources file.
    """
    sources_file = dsutils_get_sources_file()

    if not os.path.isfile(sources_file):
        dsutils_error(f"Sources file does not exist: {sources_file}")
        dsutils_error("This probably means that DSUtils has not been setup for this project.")
        dsutils_error("Please run the DSUtils setup script before continuing.")
        dsutils_error("Exiting...")
        sys.exit(1)

    with open(sources_file, 'r') as file:
        sources = file.readlines()
        return sources