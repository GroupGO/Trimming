#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A collection of functions designed to split a merged, paired-end FASTQ file into its forward and
reverse components.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


from CommandLineParser import *
import time
import sys
import os
import re


def load_fast_q_by_line(fast_q_file):
    """
    Function to yield each line of a given FASTQ file, one at a time.

    :param fast_q_file: The name of the input FASTQ file, given as a string.
    :return: Yield each line of the input file as a string.
    """
    with open(fast_q_file, 'r') as input_file:
        for line in input_file:
            yield line


def extract_record(fast_q_file):
    """
    Function to yield each record of a given FASTQ file, one at a time.

    :param fast_q_file: The name of the input FASTQ file, given as a a string.
    :return: Yields the header, sequence and quality sequence per record, as a list of strings.
    """
    header, sequence, quality = '', '', ''
    for line in load_fast_q_by_line(fast_q_file):
        line = line.strip()
        if line[0] == '@':
            header = line
        elif header and not sequence:
            sequence = line
        elif header and sequence and not quality:
            if line[0] != '+':
                quality = line
        if header and sequence and quality:
            yield header, sequence, quality
            header, sequence, quality = '', '', ''


def split_record(output_files, header, sequence, quality):
    """
    Function to split the contents of a merged FASTQ file into its forward and reverse components.

    :param output_files: The open output files, given as a list of strings.
    :param header: The header of the merged FASTQ file, given as a string.
    :param sequence: The sequence of the merged FASTQ file, given as a string.
    :param quality: The quality of the merged FASTQ file, given as a string.
    """
    seq_len = len(sequence)
    for index, lengths in enumerate([(0, seq_len/2), (seq_len/2, seq_len)]):
        start, end = lengths
        output = output_files[index]
        output.write('%s\n%s\n+\n%s\n' % (header, sequence[start:end], quality[start:end]))


def create_empty_folder(folder_name):
    """
    Method to create an empty folder to store the files.

    :param folder_name: The name of the folder to be created.
    """
    if not os.path.exists(folder_name):
        execute_on_command_line('mkdir %s' % folder_name)


def generate_output_paths(input_path, output_folder):
    """
    Function generate the output paths of the output files using the input file and output folder.

    :param input_path: The path of the input file, given as a string.
    :param output_folder: The name of the output folder, given as a string.
    :return: The output paths of forward and reverse FASTQ files, given as a list of strings.
    """
    split_name = re.split('\.|/', input_path)
    extension = split_name[-1]
    output_paths = ['', '']
    for index, name in enumerate(['forward', 'reverse']):
        output_paths[index] = '%s/%s_%s.%s' %\
                              (output_folder, '.'.join(split_name[-2:-1]), name, extension)
    return output_paths


def split_merged_data_set(input_path, output_folder, overwrite=True):
    """
    Method to split a merged, paired-end FASTQ read files into separate forward and reverse
    FASTQ files.

    :param input_path: The path of the merged, paired-end FASTQ file, given as a string.
    :param output_folder: The name of the output folder, given as a string.
    :param overwrite: A setting to overwrite existing split data stored in the same path.
    """
    assert isinstance(input_path, str), 'Input Path must be of type string.'
    assert isinstance(output_folder, str), 'Output Folder name must be of type string.'
    create_empty_folder(output_folder)
    output_paths = generate_output_paths(input_path, output_folder)
    if not all(os.path.exists(path) for path in output_paths) or overwrite:
        output_files = [open(output, 'w') for output in output_paths]
        for header, sequence, quality in extract_record(input_path):
            split_record(output_files, header, sequence, quality)


if __name__ == '__main__':
    input_file_path = '/home/jongh020/project/RNAseq/SRP041695/SRR1271857.fastq'
    output_folder_name = 'Test_Output'
    start_time = time.clock()
    print('Started paired-end read file splitting.')
    split_merged_data_set(input_file_path, output_folder_name)
    print('Completed paired-end read file splitting in %s seconds.' % (time.clock() - start_time))
