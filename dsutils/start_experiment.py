from dsutils.internals import *
import os, sys
import argparse
import re


parser = argparse.ArgumentParser(description='Starts a new experiment.')
parser.add_argument('-n', '--name', default=None, help='The name of the experiment.')
parser.add_argument('-d', '--description', default="", help='The description of the experiment.')
args = parser.parse_args()

NAME = args.name
DESCRIPTION = args.description


def __validate_NAME__(name: str | None = None):
    errors = []

    existing_experiments = os.listdir(dsutils_get_experiments_dir())
    allowed_chars = r"[a-zA-Z0-9\s_\-]"

    if name == "" or name is None:
        errors.append("Experiment name cannot be empty.")
    if name is not None and len(name) > 50:
        errors.append("Experiment name cannot be longer than 50 characters.")
    if name is not None and not re.match(allowed_chars + "+", name):
        errors.append("Experiment name can only contain alphanumeric characters, whitespace, underscores, and hyphens.")
    if name is not None and name.lower() in [experiment.lower() for experiment in existing_experiments]:
        errors.append("An experiment with this name already exists.")
    
    return errors


def __validate_DESCRIPTION__(description: str | None = None):
    errors = []
    if description == "" or description is None:
        errors.append("Experiment description cannot be empty.")

    return errors


def __generate_notebook_content__(name: str, description: str):
    name = name.strip()
    name = name.replace("_", " ")
    name = name.replace("-", " ")
    name = name.title()

    description = description.strip()

    env_vars = dsutils_read_env()
    for k, v in env_vars.items():
        env_vars[k] = v.replace(os.sep, f"{os.sep}{os.sep}")

    project_dir = env_vars["PROJECT_ROOT"]
    experiments_dir = env_vars["EXPERIMENTS_DIR"]
    data_dir = env_vars["DATA_DIR"]
    processed_dir = env_vars["DATA_PROCESSED_DIR"]
    raw_dir = env_vars["DATA_RAW_DIR"]
    artifacts_dir = env_vars["ARTIFACTS_DIR"]
    sources_file = env_vars["SOURCES_FILE"]

    content = """{
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# """ + name + """\\n",
                "\\n",
                \"""" + description + """\"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": null,
            "metadata": {},
            "outputs": [],
            "source": [
                "# DSUtils - ENV variables\\n",
                "import os",
                "import sys\\n",
                "\\n",
                "# Paths to project files & directories\\n",
                "project_dir = r'""" + project_dir + """'\\n",
                "experiments_dir = project_dir + r'""" + experiments_dir + """'\\n",
                "data_dir = project_dir + r'""" + data_dir + """'\\n",
                "processed_dir = project_dir + r'""" + processed_dir + """'\\n",
                "raw_dir = project_dir + r'""" + raw_dir + """'\\n",
                "artifacts_dir = project_dir + r'""" + artifacts_dir + """'\\n",
                "sources_file = project_dir + r'""" + sources_file + """'\\n",
                "\\n",
                "# Add directories to path\\n",
                "sys.path.append(project_dir)\\n",
                "sys.path.append(experiments_dir)\\n",
                "sys.path.append(data_dir)\\n",
                "sys.path.append(processed_dir)\\n",
                "sys.path.append(raw_dir)\\n",
                "sys.path.append(artifacts_dir)"
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}
"""
    return content


def start_experiment(name: str | None = None, description: str | None = None):
    """
    Creates a new experiment directory and notebook.

    Parameters
    ----------
    name : str | None
        The name of the experiment.
    description : str | None
        The description of the experiment.

    Returns
    -------
    dir_path : str
        The path to the newly created experiment directory.

    Raises
    ------
    FileNotFoundError
        If the experiments directory does not exist.
    ValueError
        If any arguments are invalid.
        Only raised when called from another script.
    """
    global NAME, DESCRIPTION

    try:

        # Verify experiments directory exists
        experiments_dir = dsutils_get_experiments_dir()
        if not os.path.exists(experiments_dir):
            dsutils_error("The experiments directory does not exist.")
            dsutils_error("This probably means that DSUtils has not been setup for this project.")
            dsutils_error("Please run the DSUtils setup script before continuing.")
            raise FileNotFoundError(f"The experiments directory does not exist: {experiments_dir}")

        # Parse arguments
        def __parse_var__(var: str | None = None, glb = str | None):
            if var is not None:
                return var.strip()
            elif glb is not None:
                return glb.strip()
            else:
                return ""
            
        NAME = __parse_var__(name, NAME).lower().replace(" ", "_").replace("-", "_")
        DESCRIPTION = __parse_var__(description, DESCRIPTION)

        # Validate arguments
        name_errors = __validate_NAME__(NAME)
        description_errors = __validate_DESCRIPTION__(DESCRIPTION)

        # Interactive mode when called from command line
        # Will prompt user to rectify invalid arguments
        if __name__ == "__main__":
            while len(name_errors) > 0:
                for error in name_errors:
                    dsutils_warn(error)
                NAME = dsutils_input("Experiment name: ")
                NAME = NAME.strip()
                name_errors = __validate_NAME__(NAME)
            while len(description_errors) > 0:
                for error in description_errors:
                    dsutils_warn(error)
                DESCRIPTION = dsutils_input("Experiment description: ")
                DESCRIPTION = DESCRIPTION.strip()
                description_errors = __validate_DESCRIPTION__(DESCRIPTION)
        # Non-interactive mode when called from another script
        # Will raise ValueError if any arguments are invalid
        else:
            joined_errors = name_errors + description_errors
            if len(joined_errors) > 0:
                raise ValueError(f"Invalid argument values:\n{'\n'.join(joined_errors)}")
            
        dir_name = NAME
        notebook_name = dir_name + ".ipynb"
        dir_path = os.path.join(experiments_dir, dir_name)
        notebook_path = os.path.join(dir_path, notebook_name)

        # Verify if experiment already exists, sanity check
        if os.path.exists(dir_path) or os.path.exists(notebook_path):
            dsutils_error("An experiment directory or notebook with this name already exists.")
            dsutils_error("Please choose a different name.")
            raise FileExistsError(f"An experiment with this name already exists: {dir_name}")

        # Create experiment
        notebook_content = __generate_notebook_content__(NAME, DESCRIPTION)
        os.mkdir(dir_path)
        with open(notebook_path, "w") as f:
            f.write(notebook_content)

        # Print success message
        dsutils_success(f"Successfully created experiment: {dir_name}")
        return dir_path
    except KeyboardInterrupt:
        dsutils_error("Keyboard interrupt detected. Exiting...")
        sys.exit(1)


def __main__():
    """
    Creates a new experiment directory and notebook.
    """
    start_experiment()


if __name__ == "__main__":
    __main__()