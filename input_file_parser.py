# -*- coding: utf-8 -*-
"""Input_File_Parser.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cLzAxCjJAh1UuUkTOHBagBeVOjK9-wF8
"""

import json
import os, csv

standard_def_list = []
error_template = []

input_file='input_file.txt'
standard_def_file = 'standard_definition.json'
error_code_file = 'error_codes.json'

if os.path.exists('summary.txt'):
    os.remove('summary.txt')
if os.path.exists('report.csv'):
    os.remove('report.csv')

summary_file = open("summary.txt", "a")
report_file = open("report.csv","w", encoding='UTF8', newline='')
report_writer = csv.writer(report_file, delimiter=',', lineterminator='\n')

report_writer.writerow(["Section","Sub-Section","Given Data Type", "Expected Data Type", "Given Length", "Expected MaxLength", "Error Code"])  # Add heder in the report file

summary_file.close()
report_file.close()

def log_error(message):
    summary_file = open("summary.txt", "a")
    summary_file.writelines(message)
    summary_file.close()

def getInputData(input_file):   #To get the Input data from file
    try:
        with open(input_file) as file:
            input_lines = file.readlines()
            input_lines = [line.rstrip() for line in input_lines]
            
            if input_lines == '':
                log_error('No input provided in the input_file.txt')
            return input_lines
    except Exception as Ex:
        log_error(str(Ex)+'\n')

def getStandardDef(standard_def_file):      #To get the Definition information from file
    try:
        with open(standard_def_file, 'r') as file:
          standard_def = json.load(file)
          if input_lines == '':
              log_error('No standard definition provided in the standard_definition.json')

          return standard_def
    except Exception as Ex:
        log_error(str(Ex)+'\n')

def getErrorCode(error_code_file):        #To get the Error code information from file
    try:
        with open(error_code_file, 'r') as code_file:
            error_code_list = json.load(code_file)

            for code in error_code_list:      # Append errror template in the list to write template acccording to the error_code and index of the list
                error_template.append(code['message_template'])
            if not error_template:
                log_error('No error template in the error_codes.json')

            return error_template
    except Exception as Ex:
        log_error(str(Ex)+'\n')
        
def writeSummaryReport(error_code):       # To write report and summery file according to the error_code

    summary_file = open("summary.txt", "a")
    report_file = open("report.csv","a", encoding='UTF8', newline='')
    report_writer = csv.writer(report_file, delimiter=',', lineterminator='\n')

    error_code = 'E01' if error_code == '' else error_code
    error_code = 'E04' if error_code == 'E02E03' else error_code

    if error_code == 'E02' or error_code == 'E03':
        # print(error_code, error_template[int(error_code[1:])-1].replace('LXY',key+str(elem+1)).replace('LX',key).format(data_type = defs['sub_sections'][elem]['data_type'], max_length = str(defs['sub_sections'][elem]['max_length'])))
        summary_file.writelines(error_template[int(error_code[1:])-1].replace('LXY',key+str(elem+1)).replace('LX',key).format(data_type = defs['sub_sections'][elem]['data_type'], max_length = str(defs['sub_sections'][elem]['max_length']))+'\n')
    else:
        # print(error_code, error_template[int(error_code[1:])-1].replace('LXY',key+str(elem+1)).replace('LX',key))
        summary_file.writelines(error_template[int(error_code[1:])-1].replace('LXY',key+str(elem+1)).replace('LX',key)+'\n')

    if error_code == 'E05':
        report_writer.writerow([str(key), str(defs['sub_sections'][elem]['key']), '', str(defs['sub_sections'][elem]['data_type']), '', str(defs['sub_sections'][elem]['max_length']), str(error_code)])
    else:
        report_writer.writerow([str(key), str(defs['sub_sections'][elem]['key']), str(data_type), str(defs['sub_sections'][elem]['data_type']), str(len(input_list[elem+1])) if input_list[elem+1] != '' else '', str(defs['sub_sections'][elem]['max_length']), str(error_code)])

    summary_file.close()
    report_file.close()

input_lines = getInputData(input_file)
standard_def = getStandardDef(standard_def_file)
error_template = getErrorCode(error_code_file)

try:
    for line in input_lines:  

        input_list = line.split('&')   #Split input into list

        key = input_list[0]  #Gets the first value as a key
      
        for defs in standard_def:    # Loop through all definition
            if defs['key'] == key:   # Check for particular Key from definition list

                for elem in range(0, len(defs['sub_sections'])):  #Loop through all the sub keys

                    try:
                        print(input_list[elem+1], defs['sub_sections'][elem])
                        error_code = ''

                        # if defs['sub_sections'][elem]['data_type'] == 'digits':
                        
                        if input_list[elem+1].isdigit():
                            data_type = 'digits' 
                        elif all(x.isalpha() or x.isspace() for x in input_list[elem+1]):
                            data_type = 'word_characters'
                        else:
                            data_type = 'others'

                        if input_list[elem+1] == '':
                            error_code = 'E04'
                            continue

                        if data_type != defs['sub_sections'][elem]['data_type']:
                            error_code += 'E02'

                        if len(input_list[elem+1]) > int(defs['sub_sections'][elem]['max_length']):
                            error_code += 'E03'

                    except IndexError as Ex:
                        error_code = 'E05'
                    except Exception as Ex:
                        # error_code += 'E02'
                        log_error(str(Ex)+'\n')
                    finally:
                        writeSummaryReport(error_code)    # Call function to write report and summary according to the error_code

                log_error('\n')   #To add blank line in the summary file after each section
                print('\n')

except Exception as Ex:
    log_error(str(Ex)+'\n')