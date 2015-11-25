#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A collection of function for the loading of folders, their contents and files.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


import os


def get_folder_contents_paths(folder_path, file_type):
    """
    Function to load all file names of a certain type in a given folder.

    :param folder_path: The path leading to the folder whose contents are to be extracted.,
    given as a string.
    :param file_type: The file type to be extracted given as a string.
    :return: A list of strings, containing the found files of the correct type in the given
    folder.
    """
    path_assertion(folder_path)
    found_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.%s' % file_type):
            found_files.append('%s/%s' % (folder_path, file_name))
    return found_files


def path_assertion(path):
    """
    A method to assert the presence of a directory in the current directory.

    :param path: The path to be inspected, given as a string.
    """
    assert isinstance(path, str), '%s is not of type string.'
    assert os.path.exists(path), '%s does not exist.'
