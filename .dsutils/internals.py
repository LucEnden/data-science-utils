import os
import sys
import argparse
from datetime import datetime


ENV_FILE = f"{os.path.abspath(os.path.dirname(__file__))}{os.path.sep}.dsutils.env"



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


def __parse_logoptions__(options: list[LogOptions] = []):
    # If no options are provided, default to white
    if len(options) == 0:
        options = [ LogOptions.clr_WHITE ]

    # Remove END option if it exists
    if LogOptions.END in options:
        options.remove(LogOptions.END)

    join_options = "".join(options)
    return join_options


def __dfutils_log__(message: str, options: list[LogOptions] = []):
    print(f"{__parse_logoptions__(options)}[DSUTILS | {datetime.now().strftime('%H:%M:%S')}]:{LogOptions.END} {message}")


def dsutils_info(message: str):
    __dfutils_log__(message, [ LogOptions.clr_WHITE ])


def dsutils_success(message: str):
    __dfutils_log__(message, [ LogOptions.clr_GREEN, LogOptions.trs_BOLD, LogOptions.trs_UNDERLINE ])


def dsutils_warn(message: str):
    __dfutils_log__(message, [ LogOptions.clr_YELLOW, LogOptions.trs_BOLD, LogOptions.trs_UNDERLINE ])
    

def dsutils_error(message: str):
    __dfutils_log__(message, [ LogOptions.clr_RED, LogOptions.trs_BOLD, LogOptions.trs_UNDERLINE ])


def dsutils_input(message: str, options: list[LogOptions] = []):
    return input(f"{__parse_logoptions__(options)}[DSUTILS | {datetime.now().strftime('%H:%M:%S')}]:{LogOptions.END} {message}")

#endregion


def dsutils_read_env():
    ENV_FILE = ".dsutils.env"
    if not os.path.isfile(ENV_FILE):
        dsutils_error("Environment file does not exist. Please run the initialization script before continuing.")
        dsutils_error("Exiting...")
        sys.exit(1)

    with open(ENV_FILE) as f:
        env_vars = f.read().splitlines()
        env_dict = {}
        for v in env_vars:
            env_dict[v.split("=")[0]] = v.split("=")[1]

    return env_dict