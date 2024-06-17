"""
File for various utility functions
"""

import yaml


def load_config(file_path: str):
    """
    Load a YAML configuration file from the specified path
    :param file_path: Relative from project root directory
    :return: God knows
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
