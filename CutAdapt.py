#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A class to run CutAdapt on a single input file at a time.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (

https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


from FileHandler import *
from CommandLineParser import *
import re


class CutAdapt:
    """
    A class to run CutAdapt on a single input file at a time.
    """

    def __init__(self, read_file_path, output_folder, adapter_file_path, settings):
        """
        Method to initialize the CutAdapt class in order to run CutAdapt through command line.

        :param read_file_path: The path, given as a string, leading to a RNASeq reads file.
        :param output_folder: Name of the folder in which the output will be stored,
        given as a string.
        :param adapter_file_path: Path leading to the adapter sequences file, given as a string.
        :param settings: A list of settings, given as a list of string.
        """
        assert isinstance(output_folder, str), 'Given Output folder not of type string.'
        path_assertion(read_file_path), path_assertion(adapter_file_path)
        self.output_folder, self.read_file_path = output_folder, read_file_path
        self.adapter_file, self.settings = adapter_file_path, settings
        self.output_file = self.create_output_file_name()
        self.trim_reads()

    def trim_reads(self):
        """
        Method to trim all read files contained within self.read_file_paths and save them in the
        given output folder directory under the same name.

        """
        if not os.path.isdir(self.output_file):
            execute_on_command_line('mkdir %s' % self.output_file)
        execute_on_command_line(self.build_command_string)

    def build_command_string(self):
        """
        Function to build the CutAdapt command line string and return it as a string.

        :return: A command line string to launch CutAdapt and trim the given input sequences
        using the given adapter sequences.
        """
        output_path = '%s/%s' % (self.output_file, self.output_file)
        cmd_string = 'cutadapt -a file:%s -o %s %s' % \
            (self.adapter_file, output_path, self.read_file_path)
        return cmd_string

    def create_output_file_name(self):
        """
        Function to create an output file name using the file path, i.e.
            '/folder/file.fasta' >> 'file.trim.fasta'

        :return: The output file name.
        """
        file_name = re.findall(self.read_file_path, '/(w+\.w+/?)$')[0]
        file_contents = file_name.split('.')
        file_name = file_contents[0] + '.trim.' + file_contents[1]
        return file_name
