# DSUtils
A comprehensive collection of utilities designed to supercharge my (and hopefully others) data science workflow.

## EARLY STAGE
This project is in the early stages of development. The utilities are not yet fully implemented, and the documentation is not yet complete. The project is being developed in my free time, so progress may be slow.

## Design

The utilities are designed to be used within a Anaconda environment using Jupyter notebooks.
They are also designed with a particular workflow in mind. The workflow is as follows:
- As a data scientist, you perform experiments on data.
- Some experiments are successful, and you want to save the results.
- You want to be able to easily access the results of succesfull experiments.

In order to facilitate this workflow, the utilities are designed to easily save and load the results of experiments. The results are saved in a directory structure that is easy to navigate and understand. The directory structure is as follows:
```
- <project>
    - artifacts
    - data
        - raw
        - processed
    - experiments
        - <experiment>
            - <experiment>.ipynb
    - sources.csv
    - <other project files>
```

## Installation
...

## Usage
...