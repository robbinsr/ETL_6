import os
import re
from collections import OrderedDict
import pandas as pd

"""
This program reads an IHIS codebook file (https://www.ihis.us).
writes a set of csv files that can be used to load one Oracle table per csv file.
Author: Russ Robbins russ.robbins@outlook.com
"""

# SHOW CURRENT DIRECTORY
# print(os.getcwd())

# INPUT FILES
codebook_FILE = './input_data/ihis_household_1997_2014.cbk'

# OUTPUT FILES

README_FILE = "./read_codebook_README.md"
samples_FILE = './SAMPLES_NAMES_AND_TYPES.csv' # indicates years that were sampled and data shape
coded_data_by_sample_availability_key_FILE = './CODED_DATA_BY_SAMPLE_KEY.csv'
coded_data_by_sample_info_FILE = './CODED_DATA_BY_SAMPLE_INFO.csv'
code_definitions_FILE = './CODE_DEFINITIONS.csv'

# ... other files of the form <CODE> + _CODE_VALUES.csv
# ... will be written to provide values per code and the values' meanings.

# STRINGS TO INDICATE WHERE IN FILE INFORMATION EXISTS

file_desc_tag_STR = str()
file_type_tag_STR = str()
samples_in_tag_STR = str()
cases_selected_tag_STR = str()
variable_availability_key_tag_STR = str()
codes_values_section_tags_STR = str()
code_description_STR = str()

# STRINGS TO GENERATE DYNAMIC OBJECTS
# or EXPRESSIONS BASED ON FILE
dynamic_code_values_dict_name_STR = str()
assign_dynamic_code_values_dict_STR = str()
declare_dynamic_code_values_dict_STR = str()

dynamic_code_value_df_name_STR = str()
assign_dynamic_code_values_df_STR = str()
declare_dynamic_code_values_df_STR = str()

dynamic_code_value_csv_filename_STR = str()
execute_write_csv_STR = str()

# INTS
sampls_bgn_lne_INT = int()
smpls_end_lne_INT = int()
variables_by_smpls_bgn_lne_INT = int()
variables_by_smpls_end_lne_INT = int()
variables_by_samples_column_titles_line_INT = int()
vrble_avlblty_ky_begin_line_INT = int()
# vrble_avlblty_ky_end_line_INT = int() # decared inline below
code_value_section_header_line_number_INT = int()
code_value_section_detail_begin_line_number_INT = int()
code_value_section_detail_end_line_number_INT = int()

# BOOLS
cases_selected_BOOL = bool

# TUPLES
file_desc_TUPLE = ()
file_type_TUPLE = ()
samples_begin_TUPLE = ()
samples_end_TUPLE = ()
samples_begin_end_TUPLE = ()
cases_selected_TUPLE = ()
# variable_availability_key_TUPLE = ()
variables_by_samples_TUPLE = ()

# LISTS

# ...the commented lists below are declared inline below

# samples_in_LIST = list()
# variables_by_samples_LIST = list()
# variables_by_samples_column_titles_LIST = list()

codebook_readme_LIST = list()
codes_defns_starts_ends_LIST = list()
code_descs_LIST = list()
code_values_descs_LIST = list()

row_LIST = list()

# DICTIONARIES
samples_names_and_types_DICT = OrderedDict()
variables_by_samples_DICT = OrderedDict()
data_file_meta_data_DICT = OrderedDict()
variable_availability_key_DICT = OrderedDict()

# PANDAS DATAFRAMES

# ...the commented dataframes below are declared inline below

# samples_names_and_types_DF = pd.DataFrame()
# variable_availability_key_DF = pd.DataFrame()
# variables_by_samples_DF = pd.DataFrame()

# ...dynamically named dataframes are also declared below

# REGULAR EXPRESSION STRING PATTERNS
column_name_RE = re.compile('^\s([A-Z0-9]+)\s*([\w\W]+)$')
file_description_RE = re.compile('^(Description:)\s(.*)$')
samples_tag_RE = re.compile('(^Samples selected:)\s.*$')
sample_name_and_type_RE = re.compile('^\s*([]A-Z0-9]*\s[A-Z0-9]*)\s*([a-z]*)$')
file_type_tag_RE = re.compile('^(File Type:)\s*(.*)$')
cases_selected_tag_RE = re.compile('^(Case\sSelection:)\s*(.*)$')
variable_availability_key_tag_RE = re.compile('^(Variable Availability Key:)')
variability_availability_codes_RE = re.compile(
    '^(All Years)\s(X|\.) - ([]\w+\s]+)$')
variables_by_sample_RE = re.compile(
    '^\s{2}([A-Z0-9]+)\s+[0-9]\s+([0-9-]+)\s+([0-9]+)[\s]{6}(.*)')
codes_values_section_tags_RE = re.compile('^\s([A-Z0-9]+)\s+(.*)')
value_desc_RE = re.compile('^([0-9]+)\s+(.+)')


# OPEN FILE THAT DESCRIBES DATA FILE

with open(codebook_FILE, mode='r+') as codebook_file_in:
    # FILE IS SMALL ... READ WHOLE FILE
    codebook = codebook_file_in.readlines()

    # FOR EACH LINE IN FILE, AND KEEP TRACK OF LINE NUMBER AS INDEX
    for index, line in enumerate(codebook):

        # FIND AND STORE FILE DESCRIPTION
        file_desc_SEARCH = re.search(file_description_RE, line)
        if file_desc_SEARCH:
            file_desc_tag_STR = file_desc_SEARCH.group(1)
            file_description = file_desc_SEARCH.group(2)
            file_desc_TUPLE = (file_desc_tag_STR, file_description)
            codebook_readme_LIST.append(file_desc_TUPLE)

        # FIND AND STORE SAMPLES BEGIN LINE
        samples_selected_tag_SEARCH = re.search(samples_tag_RE, line)
        if samples_selected_tag_SEARCH:
            samples_in_tag_STR = samples_selected_tag_SEARCH.group(1)
            sampls_bgn_lne_INT = int(index + 1)
            samples_begin_TUPLE = ("SAMPLES BEGIN LINE", sampls_bgn_lne_INT)

        # FIND FILE TYPE
        file_type_SEARCH = re.search(file_type_tag_RE, line)
        if file_type_SEARCH:
            # STORE FILE TYPE
            file_type_tag_STR = file_type_SEARCH.group(1)
            file_type = file_type_SEARCH.group(2)
            file_type_TUPLE = (file_type_tag_STR, file_type)
            codebook_readme_LIST.append(file_type_TUPLE)

            # INFER SAMPLES END LINE
            smpls_end_lne_INT = int(index)

            # STORE SAMPLES END LINE
            samples_end_TUPLE = ("SAMPLES END LINE", smpls_end_lne_INT)
            samples_begin_end_TUPLE = (samples_begin_TUPLE, samples_end_TUPLE)

        # FIND OUT AND STORE WHETHER CASES WERE SELECTED
        # AND SET VARIABLES BY SAMPLES SECTION BEGIN LINE and COLUMNS LINE
        cases_selected_SEARCH = re.search(cases_selected_tag_RE, line)
        if cases_selected_SEARCH:
            cases_selected_tag_STR = cases_selected_SEARCH.group(1)
            cases_selected_value = cases_selected_SEARCH.group(2)
            if cases_selected_value == 'yes':
                cases_selected_BOOL = True
            else:
                cases_selected_BOOL = False

            cases_selected_TUPLE = (cases_selected_tag_STR, cases_selected_BOOL)
            codebook_readme_LIST.append(cases_selected_TUPLE)

            variables_by_samples_column_titles_line_INT = index + 1
            variables_by_smpls_bgn_lne_INT = index + 2

        # FIND AND STORE VARIABLES BY SAMPLES SECTION END LINE AND
        # AND FIND VARIABILITY_AVAILABILITY_KEY_BEGIN_LINE
        samples_selected_tag_SEARCH = re.search(
            variable_availability_key_tag_RE, line)
        if samples_selected_tag_SEARCH:
            variable_availability_key_tag_STR = samples_selected_tag_SEARCH.group(1)
            variables_by_smpls_end_lne_INT = index - 1
            vrble_avlblty_ky_begin_line_INT = index + 1

        # FIND AND STORE LINE NUMBERS WHERE CODE VALUES SECTIONS ARE TAGGED
        codes_values_section_tags_SEARCH = re.search(
            codes_values_section_tags_RE, line)
        if codes_values_section_tags_SEARCH:
            code_value_section_header_line_number_INT = index
            code_value_section_detail_begin_line_number_INT = index + 1
            codes_values_section_tags_STR = codes_values_section_tags_SEARCH.group(1)
            code_description_STR = codes_values_section_tags_SEARCH.group(2)
            codes_defns_starts_ends_LIST.append(
                [codes_values_section_tags_STR, code_description_STR,
                 code_value_section_header_line_number_INT,
                 code_value_section_detail_begin_line_number_INT])

    # FIND AND STORE VARIABILITY_AVAILABILITY_KEY_END_LINE
    vrble_avlblty_ky_end_line_INT = codes_defns_starts_ends_LIST[0][2] - 2
    variable_availability_key_TUPLE = (vrble_avlblty_ky_begin_line_INT, vrble_avlblty_ky_end_line_INT)

    # FIND AND STORE SAMPLES META DATA
    samples_in_LIST = codebook[sampls_bgn_lne_INT: smpls_end_lne_INT]
    for line_number, line in enumerate(samples_in_LIST):
        sample_name_and_type_SEARCH = re.search(sample_name_and_type_RE, line)
        samples_names_and_types_DICT[sample_name_and_type_SEARCH.group(
            1)] = sample_name_and_type_SEARCH.group(2)

    # FIND AND STORE COLUMN NAMES FOR VARIABLES BY SAMPLES META DATA
    variables_by_samples_column_titles_LIST = codebook[
        variables_by_samples_column_titles_line_INT]
    column_names = re.search(
        '^\s{2}(Variable)\s{15}(Columns)\s{8}(Len)\s{4}(.*)$',
        variables_by_samples_column_titles_LIST)
    variables_by_samples_columns_LIST = [column_names.group(1),
                                         column_names.group(2),
                                         column_names.group(3)]
    split_columns = column_names.group(4).split()

    for column in split_columns:
        variables_by_samples_columns_LIST.append(column)

    # FIND AND STORE VARIABLES BY SAMPLES META DATA
    variables_by_samples_LIST = \
        codebook[variables_by_smpls_bgn_lne_INT:variables_by_smpls_end_lne_INT]

    for line_number, line in enumerate(variables_by_samples_LIST):
        row_SEARCH = re.search(variables_by_sample_RE, line)
        split_row = row_SEARCH.group(4).split()
        row_LIST = [row_SEARCH.group(1), row_SEARCH.group(2),
                    row_SEARCH.group(3)] + split_row
        variables_by_samples_DICT[str(line_number)] = row_LIST

    # FIND AND STORE VARIABLE AVAILABILITY KEY META DATA
    variable_availability_key_LIST = \
        codebook[vrble_avlblty_ky_begin_line_INT:vrble_avlblty_ky_end_line_INT]
    for line_number, line in enumerate(variable_availability_key_LIST):
        row_SEARCH = re.search(variability_availability_codes_RE, line)
        row_LIST = [row_SEARCH.group(2), row_SEARCH.group(3)]
        variable_availability_key_DICT[str(line_number)] = row_LIST

    # LOOP THROUGH codes_defns_starts_ends_LIST,
    # AND CREATE DATAFRAMES FOR EACH CODE'S VALUES AND THEIR DESCRIPTIONS
    # AND WRITE CSV FILES FOR EACH DATAFRAME

    for index, element in enumerate(codes_defns_starts_ends_LIST):
        # print(index, element)
        if index != 0 and index != len(codes_defns_starts_ends_LIST):
            codes_defns_starts_ends_LIST[index - 1].append(codes_defns_starts_ends_LIST[index][2] - 1)
        if index == len(codes_defns_starts_ends_LIST) - 1:
            codes_defns_starts_ends_LIST[index].append(len(codebook))
        code_descs_LIST.append((element[0], element[1]))

    for index, element in enumerate(codes_defns_starts_ends_LIST):
        code_values_start_line_INT = element[3]
        code_values_end_line_INT = element[4]
        code_values_descs_LIST = codebook[code_values_start_line_INT:code_values_end_line_INT]
        dynamic_code_values_dict_name_STR = element[0] + '_DICT'
        dynamic_code_value_df_name_STR = element[0] + '_DF'
        assign_dynamic_code_values_df_STR = ' = dict()'
        declare_dynamic_code_values_dict_STR = dynamic_code_values_dict_name_STR + assign_dynamic_code_values_df_STR
        exec declare_dynamic_code_values_dict_STR

        for value_desc in code_values_descs_LIST:
            value_desc_SEARCH = re.search(value_desc_RE, value_desc)
            if value_desc_SEARCH:
                key = str(re.escape(value_desc_SEARCH.group(1).strip()))
                value = str(re.escape(value_desc_SEARCH.group(2).strip()))

                assign_dynamic_code_values_dict_STR = dynamic_code_values_dict_name_STR + '[' + "'" + str(
                    key) + "'" + ']' + '=' + "'" + str(value) + "'"
                assert (isinstance(assign_dynamic_code_values_dict_STR, str))
                exec assign_dynamic_code_values_dict_STR

                assign_dynamic_code_values_df_STR = '= pd.DataFrame(' + dynamic_code_values_dict_name_STR \
                                                    + '.items(),' \
                                                    + ' columns = [\'CODE_VALUE\', \'CODE_DESCRIPTION\'])'
                declare_dynamic_code_values_df_STR = dynamic_code_value_df_name_STR + assign_dynamic_code_values_df_STR
                assert (isinstance(declare_dynamic_code_values_df_STR, str))
                exec declare_dynamic_code_values_df_STR

                dynamic_code_value_csv_filename_STR = 'CODE_VALUES_' + element[0]
                execute_write_csv_STR = dynamic_code_value_df_name_STR + '.to_csv(' + "'" + \
                                        dynamic_code_value_csv_filename_STR + '.csv' + "'" + ', index=None)'
                assert isinstance(execute_write_csv_STR, str)
                exec execute_write_csv_STR

    # WRITE codes_descs_LIST to DF THEN TO CSV FILE

    code_descs_DF = pd.DataFrame(code_descs_LIST, columns=['CODE_NAME', 'CODE_DEFINITION'])

    code_descs_DF.to_csv('CODE_DEFINITIONS.csv', index=None)

    # WRITE Samples_names_and_types_DICT TO DF THEN TO CSV FILE

    samples_names_and_types_DF = pd.DataFrame(samples_names_and_types_DICT.items(),
                                              columns=['SAMPLE_NAME', 'SAMPLE_TYPE'])

    samples_names_and_types_DF.to_csv(samples_FILE, index=None)

    # WRITE variable_availability_key_DICT TO DF THEN TO CSV FILE

    variable_availability_key_DF = pd.DataFrame(
        variable_availability_key_DICT.values(),
        columns=['CELL_VALUE', 'CELL_DESCRIPTION'],
        index=variable_availability_key_DICT.keys())

    variable_availability_key_DF.to_csv()
    variable_availability_key_DF.to_csv(coded_data_by_sample_availability_key_FILE, index=None)

    # WRITE variables_by_samples_DICT TO DF THEN TO CSV FILE

    variables_by_samples_DF = pd.DataFrame(variables_by_samples_DICT.values(),
                                           columns=variables_by_samples_columns_LIST,
                                           index=variables_by_samples_DICT.keys())

    variables_by_samples_DF.to_csv(coded_data_by_sample_info_FILE, index=None)

    # WRITE codebook_summary_file to TXT file

    with open(README_FILE, mode='w') as f_out:
        f_out.writelines('This file was created by read_codebook.py .\n')
        f_out.writelines('This file was built using data in the file ending with the *.cbk file extension.\n')
        f_out.writelines('The *.cbk file is the codebook for the *.dat file with the same name as the .cbk file.\n')
        f_out.writelines('The codebook provides information about code values that are used in the *.dat file\'s columns.\n')
        f_out.writelines('CODE_DEFINITIONS.csv provides the definitions for each code-based column in the *.dat file.\n')
        f_out.writelines('The other types of columns provide identification numbers or numerical values.\n')
        f_out.writelines('Each code has an affiliated CSV file whose name begins with the CODE and ends with CODE_VALUES.\n')
        f_out.writelines('The CODE_VALUES.csv files provide the possible values for each code, as well as the values\' definitions.\n')
        f_out.writelines('The SAMPLES_NAMES_AND_TYPES.csv indicates the years from which samples were taken when the *.dat file was generated by IHIS.\n')
        f_out.writelines('The CODED_DATA_BY_SAMPLE_KEY.csv file indicates how to interpret cells in the CODED_DATA_BY_SAMPLE_INFO.csv file.\n')
        f_out.writelines('Information that is below this line describes the *.dat file.\n\n')

        for line in codebook_readme_LIST:
            file_line = str(line) + '\n'
            f_out.writelines(file_line)
