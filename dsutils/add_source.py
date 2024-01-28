# Add the dsutils directory to the path so that we can import from it when running this file directly
import os, sys
if __name__ == "__main__":
    dsutils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, dsutils_path)

from dsutils.internals import *
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Adds a new source entry to the sources.csv file.')

#"id,name,type,description,url,citation"
parser.add_argument('-n', '--name', default=None, help='The name of the source.')
parser.add_argument('-d', '--description', default=None, help='The description of the source.')
parser.add_argument('-u', '--url', default=None, help='The url of the source.')
parser.add_argument('-c', '--citation', default=None, help='The citation for the source.')

args = parser.parse_args()
NAME = args.name
DESCRIPTION = args.description
URL = args.url
CITATION = args.citation

PROJECT_ROOT = dsutils_get_project_root()
SOURCES_FILE = os.path.join(PROJECT_ROOT, "sources.csv")


def __validate_NAME__(name: str | None = None):
    """
    Validates the name argument.

    Args:
    ----------
    name : str, optional
        The name of the source, default None

    Returns:
    -------
    list
        A list of error messages, empty if no errors are found.
    """
    errors = []

    existing_sources = dsutils_get_sources_file_content()

    if name == "" or name is None:
        errors.append("Source name cannot be empty.")
    if name.isalnum() == False:
        errors.append("Source name must contain only alphanumeric characters (a-z, A-Z, 0-9).")
    if len(existing_sources) > 1 and any([ line.startswith(name) for line in existing_sources[1:] ]):
        errors.append(f"Source with name '{name}' already exists.")

    return errors


def __validate_DESCRIPTION__(description: str | None = None):
    """
    Validates the description argument.
    
    Args:
    ----------
    description : str, optional
        The description of the source, default None

    Returns:
    -------
    list
        A list of error messages, empty if no errors are found.
    """
    errors = []

    if description == "" or description is None:
        errors.append("Source description cannot be empty.")

    return errors


def __validate_URL__(url: str | None = None):
    """
    Validates the URL argument.
    
    Args:
    ----------
    url : str, optional
        The url of the source, default None

    Returns:
    -------
    list
        A list of error messages, empty if no errors are found.
    """
    errors = []

    if url == "" or url is None:
        errors.append("Source url cannot be empty.")
    if not all([urlparse(url).scheme, urlparse(url).netloc]):
        errors.append("Source url must be a valid URL, i.e. start with 'http://' or 'https://' and contain a domain name.")

    return errors


def __validate_CITATION__(citation: str | None = None):
    """
    Validates the citation argument.
    
    Args:
    ----------
    citation : str, optional
        The citation of the source, default None

    Returns:
    -------
    list
        A list of error messages, empty if no errors are found.
    """
    errors = []

    if citation == "" or citation is None:
        errors.append("Source citation cannot be empty.")

    return errors


def add_source(name: str | None = None, description: str | None = None, url: str | None = None, citation: str | None = None):
    """
    Adds a new source entry to the sources.csv file.  
    If any of the arguments are invalid and the function is called from another script, a `ValueError` will be raised.
    If this script is called from the command line, the user will be prompted to rectify invalid arguments.

    Args:
    ----------
    name : str, optional
        The name of the source, default None
    description : str, optional
        The description of the source, default None
    url : str, optional
        The url of the source, default None
    citation : str, optional
        The citation of the source, default None

    Raises
    ------
    ValueError
        If any of the arguments are invalid and the function is called from another script.
    """
    global NAME, DESCRIPTION, URL, CITATION

    def __parse_var__(var: str | None = None, glb = str | None):
        if var is not None:
            return var.strip()
        elif glb is not None:
            return glb.strip()
        else:
            return ""
        
    NAME = __parse_var__(name, NAME)
    DESCRIPTION = __parse_var__(description, DESCRIPTION)
    URL = __parse_var__(url, URL)
    CITATION = __parse_var__(citation, CITATION)

    name_errors = __validate_NAME__(NAME)
    description_errors = __validate_DESCRIPTION__(DESCRIPTION)
    url_errors = __validate_URL__(URL)
    citation_errors = __validate_CITATION__(CITATION)

    try:
    # Interactive mode when called from command line
    # Will prompt user to rectify invalid arguments
        if __name__ == "__main__":
            while len(name_errors) > 0:
                for error in name_errors:
                    dsutils_warn(error)
                NAME = dsutils_input("Source name: ")
                NAME = NAME.strip()
                name_errors = __validate_NAME__(NAME)

            while len(description_errors) > 0:
                for error in description_errors:
                    dsutils_warn(error)
                DESCRIPTION = dsutils_input("Source description: ")
                DESCRIPTION = DESCRIPTION.strip()
                description_errors = __validate_DESCRIPTION__(DESCRIPTION)

            while len(url_errors) > 0:
                for error in url_errors:
                    dsutils_warn(error)
                URL = dsutils_input("Source URL: ")
                URL = URL.strip()
                url_errors = __validate_URL__(URL)

            while len(citation_errors) > 0:
                for error in citation_errors:
                    dsutils_warn(error)
                CITATION = dsutils_input("Source citation: ")
                CITATION = CITATION.strip()
                citation_errors = __validate_CITATION__(CITATION)

        # Non-interactive mode when called from another script
        # Will raise ValueError if any arguments are invalid
        else:
            joined_errors = name_errors + description_errors + url_errors + citation_errors
            if len(joined_errors) > 0:
                raise ValueError("Invalid argument values:\n" + '\n'.join(joined_errors))
            
        existing_sources = dsutils_get_sources_file_content()
        new_id = 0
        if len(existing_sources) > 1:
            new_id = int(existing_sources[-1].split(';')[0]) + 1

        newline = f"{new_id};'{NAME}';'{DESCRIPTION}';'{URL}';'{CITATION}'"

        with open(SOURCES_FILE, 'a') as file:
            file.write(f"\n{newline}")

        return newline
    except KeyboardInterrupt:
        dsutils_error("KeyboardInterrupt")
        sys.exit(1)


if __name__ == "__main__":
    add_source()