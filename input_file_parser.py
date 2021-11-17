# -*- coding: utf-8 -*-
"""Input_File_Parser_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g4HPlrLSHFfAIoDWupDz-BQq7sAMte3B
"""

# -*- coding: utf-8 -*-
"""Input_File_Parser.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cLzAxCjJAh1UuUkTOHBagBeVOjK9-wF8
"""

from enum import Enum
import json
import sys, os, csv

class position(Enum): 
  SECTION = 0
  SUB_SECTION = 1
  GIVEN_DATA_TYPE = 2
  EXPECTED_DATA_TYPE = 3
  GIVEN_LENGTH = 4
  EXPECTED_LENGTH = 5	
  ERROR_CODE = 6

#input_file='E:\input_parser\input_file.txt'
#standard_def_file = 'E:\input_parser\standard_definition.json'
#error_code_file = 'E:\input_parser\error_codes.json'

if os.path.exists('summary.txt'):
    os.remove('summary.txt')
if os.path.exists('report.csv'):
    os.remove('report.csv')
if os.path.exists('log_file.txt'):
    os.remove('log_file.txt')

def log_error(message):
    log_file = open("log_file.txt", "a")
    log_file.writelines(message)
    log_file.close()

def getInputData(input_file):   #To get the Input data from file
    try:
        if not os.path.exists(input_file):
            log_error('getInputData function: '+'File '+ input_file +' does not exist! \n')
        with open(input_file) as file:
            input_ = file.readlines()
        file.close()

        for line in input_:
            if not line.strip() == '':
                input_lines.append(line.rstrip())

        if input_lines == '':
            log_error('getInputData function: '+'No input provided in the input_file.txt \n')
        
        return input_lines

    except Exception as Ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_error('getInputData function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')
        return False

def getStandardDef(standard_def_file):      #To get the Definition information from file
    key = []
    values = []

    try:
        if not os.path.exists(standard_def_file):
            log_error('getStandardDef function: '+'File '+ standard_def_file +' does not exist! \n')

        with open(standard_def_file, 'r') as file:
          standard_def = json.load(file)
        file.close()

        for each_key in standard_def:
            key.append(each_key['key'])
            values.append(each_key['sub_sections'])

        return dict(zip(key,values))

    except Exception as Ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_error('getStandardDef function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')
        return False

def getErrorCode(error_code_file):        #To get the Error code information from file
    try:
        error_template = []

        if not os.path.exists(error_code_file):
            log_error('getErrorCode function: '+'File '+ standard_def_file +' does not exist! \n')

        with open(error_code_file, 'r') as code_file:
            error_code_list = json.load(code_file)

            for code in error_code_list:      # Append errror template in the list to write template acccording to the error_code and index of the list
                error_template.append(code['message_template'])
            if not error_template:
                log_error('getErrorCode function: '+'No error template in the error_codes.json \n')

            return error_template

    except Exception as Ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_error('getErrorCode function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')
        return False

def writeReport(concluded_value):       # To write report and summery file according to the error_code
    try:

        report_file = open("report.csv","w", encoding='UTF8', newline='')
        report_writer = csv.writer(report_file, delimiter=',', lineterminator='\n')

        report_writer.writerow(["Section","Sub-Section","Given Data Type", "Expected Data Type", "Given Length", "Expected MaxLength", "Error Code"])  # Add heder in the report file

        for element in concluded_value:
            if element[position.SECTION.value] == 'NEW' and element[position.SUB_SECTION.value] == 'SECTION':
                continue
            # print([element[position.SECTION.value], element[position.SUB_SECTION.value], element[position.GIVEN_DATA_TYPE.value], element[position.EXPECTED_DATA_TYPE.value], element[position.GIVEN_LENGTH.value], element[position.EXPECTED_LENGTH.value], element[position.ERROR_CODE.value]])
            report_writer.writerow([element[position.SECTION.value], element[position.SUB_SECTION.value], element[position.GIVEN_DATA_TYPE.value], element[position.EXPECTED_DATA_TYPE.value], element[position.GIVEN_LENGTH.value], element[position.EXPECTED_LENGTH.value], element[position.ERROR_CODE.value]])
        report_file.close()

        return True
    except Exception as Ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_error('writeReport function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')
        return False

def writeSummary(concluded_value, error_template):       # To write report and summery file according to the error_code
    try:
        summary_file = open("summary.txt", "a")

        for element in concluded_value:

            if element[position.SECTION.value] == 'NEW' and element[position.SUB_SECTION.value] == 'SECTION':
                summary_file.writelines('\n')
            elif element[position.ERROR_CODE.value] == 'E02' or element[position.ERROR_CODE.value] == 'E03':
                summary_file.writelines(error_template[int(element[position.ERROR_CODE.value][1:])-1].replace('LXY',element[position.SUB_SECTION.value]).replace('LX',element[position.SECTION.value]).format(data_type = element[position.EXPECTED_DATA_TYPE.value], max_length = element[position.EXPECTED_LENGTH.value])+'\n')
            else:
                summary_file.writelines(error_template[int(element[position.ERROR_CODE.value][1:])-1].replace('LXY',element[position.SUB_SECTION.value]).replace('LX',element[position.SECTION.value])+'\n')

        summary_file.close()

        return True
    except Exception as Ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_error('main function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')
        return False

def checkValidation(input_lines, standard_def):
    error_code = ''
    concluded_value = []
    input_list = []
    sub_elem_value = ''

    try:
        for line in input_lines:

            input_list = line.split('&')   #Split input into list
            key = input_list[0]  # Gets the first value as a key/Section
            sub_section = 1   # pointer to point sub_sectioni in input_list
            
            if not key in standard_def:
                continue
            
            for each_sub_section in standard_def[key]:  #Loop through all the sub Section
                try:
                    data_type = ''
                    error_code = ''
                    sub_elem_value = input_list[sub_section]  # gets the value to validate

                    # print(sub_elem_value, each_sub_section)

                    if sub_elem_value == '':  # check if value is not provided then assign data_type to others and error_code to E04
                        data_type = 'others'
                        error_code = 'E04'
                    else:
                        if sub_elem_value.isdigit():  # check if value is digit
                            data_type = 'digits' 
                        elif all(x.isalpha() or x.isspace() for x in sub_elem_value.strip()):  # check if value is word character including space
                            data_type = 'word_characters'
                        else:
                            data_type = 'others'

                        if data_type != each_sub_section['data_type']:    # check if value is digit
                            error_code = 'E02'

                        if len(sub_elem_value) > int(each_sub_section['max_length']):
                            error_code = 'E04' if error_code == 'E02' else 'E03'

                except IndexError as Ex:
                    error_code = 'E05'
                except Exception as Ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    log_error('checkValidation function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')
                finally:
                    error_code = 'E01' if error_code == '' else error_code
                    concluded_value.append([key, key+str(sub_section), data_type, each_sub_section['data_type'], '' if error_code == 'E05' else str(len(input_list[sub_section])), str(each_sub_section['max_length']), error_code])
                    # print([key, key+str(sub_section), data_type, each_sub_section['data_type'], '' if error_code == 'E05' else str(len(input_list[sub_section])), str(each_sub_section['max_length']), error_code])
                    sub_section+=1

            concluded_value.append(['NEW','SECTION'])   #To seperate summary of different section in the summary file

        return concluded_value  
    except Exception as Ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_error('checkValidation function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')

if __name__ == '__main__':

  input_lines = []
  standard_def = []
  error_template = []

  try:
      input_file = input("Enter input file name: ")
      standard_def_file = input("Enter standard definition file name: ")
      error_code_file = input("Enter error code file name: ")
	  
      input_lines = getInputData(input_file)
      if input_lines is None or input_lines == '':
          log_error('main function: '+'Error: While reading input file! \n')
          exit()

      standard_def = getStandardDef(standard_def_file)
      if standard_def is None or standard_def == '':
          log_error('main function: '+'Error: While reading standard definition file! \n')
          exit()

      concluded_value = checkValidation(input_lines, standard_def)
      if concluded_value is None or concluded_value == '':
          log_error('main function: '+'Error: While checking validation! \n')
          exit()

      error_template = getErrorCode(error_code_file)
      if error_template is None or error_template == '':
          log_error('main function: '+'Error: While reading error code file \n')
          exit()

      if not writeReport(concluded_value):    # Call function to write report and summary according to the error_code
          log_error('main function: '+'Error: While writing Report! \n')
          exit()

      if not writeSummary(concluded_value, error_template):    # Call function to write report and summary according to the error_code
          log_error('main function: '+'Error: While writing Summary! \n')
          exit()

  except Exception as Ex:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      log_error('main function: '+ str(exc_type) + ' at line no: '+str(exc_tb.tb_lineno) + ', ' + str(Ex)+'\n')
