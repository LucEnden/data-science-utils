from internals import *
import os
import re


def __create_files_and_folders__():
    envs = dsutils_read_env()
    project_root = envs["PROJECT_ROOT"]

    files_and_folders = [
        os.path.join(project_root, "artefacts"),
        os.path.join(project_root, "artefacts", "artefacts.py"),
        os.path.join(project_root, "data"),
        os.path.join(project_root, "data", "reference.csv"),
        os.path.join(project_root, "data", "processed"),
        os.path.join(project_root, "data", "raw"),
        os.path.join(project_root, "experiments")
    ]

    for f in files_and_folders:
        if os.path.isfile(f):
            dsutils_warn(f"File already exists: {f}")
        elif os.path.isdir(f):
            dsutils_warn(f"Folder already exists: {f}")
        else:
            if re.match(r".*\.\w+", f) is not None:
                with open(f, "w") as file:
                    file.write("")
            else:
                os.mkdir(f)
            dsutils_success(f"Created: {f}")
            

if __name__ == "__main__":
    __create_files_and_folders__()