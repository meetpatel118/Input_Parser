import unittest
import input_file_parser

#input_file='E:\input_parser\Input_Parser_Unittest\input_test_case.txt'
#standard_def_file = 'E:\input_parser\standard_definition.json'
#error_code_file = 'E:\input_parser\error_codes.json'

class TestClass(unittest.TestCase):

    def test_getInputData(self):
        try:
            input_value = input_file_parser.getInputData(input_file)
        except Exception as Ex:
            input_file_parser.log_error(str(Ex)+'\n')
        finally:
            self.assertEqual(input_value,['L1&1&A1', 'L2&n&0&34', 'L1&BC&wZ &', 'L3&X!', 'L4&1B&X12042&'])

    def test_getStandardDef(self):
        try:
            standard_def = input_file_parser.getStandardDef(standard_def_file)
        except Exception as Ex:
            input_file_parser.log_error(str(Ex)+'\n')
        finally:
            self.assertEqual(standard_def,{'L1': [{'key': 'L11', 'data_type': 'digits', 'max_length': 1}, {'key': 'L12', 'data_type': 'word_characters', 'max_length': 3}, {'key': 'L13', 'data_type': 'word_characters', 'max_length': 2}], 'L2': [{'key': 'L21', 'data_type': 'word_characters', 'max_length': 1}, {'key': 'L22', 'data_type': 'digits', 'max_length': 1}, {'key': 'L23', 'data_type': 'word_characters', 'max_length': 2}], 'L3': [{'key': 'L31', 'data_type': 'word_characters', 'max_length': 1}], 'L4': [{'key': 'L41', 'data_type': 'word_characters', 'max_length': 1}, {'key': 'L42', 'data_type': 'digits', 'max_length': 6}]})

    def test_checkValidation(self):
        try:
            input_value = input_file_parser.getInputData(input_file)
            standard_def = input_file_parser.getStandardDef(standard_def_file)
            concluded_value = input_file_parser.checkValidation(input_value, standard_def)
        except Exception as Ex:
            input_file_parser.log_error(str(Ex)+'\n')
        finally:
            self.assertEqual(concluded_value, [['L1', 'L11', 'digits', 'digits', '1', '1', 'E01'], ['L1', 'L12', 'others', 'word_characters', '2', '3', 'E02'], ['L1', 'L13', '', 'word_characters', '', '2', 'E05'], ['NEW', 'SECTION'], ['L2', 'L21', 'word_characters', 'word_characters', '1', '1', 'E01'], ['L2', 'L22', 'digits', 'digits', '1', '1', 'E01'], ['L2', 'L23', 'digits', 'word_characters', '2', '2', 'E02'], ['NEW', 'SECTION'], ['L1', 'L11', 'word_characters', 'digits', '2', '1', 'E04'], ['L1', 'L12', 'word_characters', 'word_characters', '3', '3', 'E01'], ['L1', 'L13', 'others', 'word_characters', '0', '2', 'E04'], ['NEW', 'SECTION'], ['L3', 'L31', 'others', 'word_characters', '2', '1', 'E04'], ['NEW', 'SECTION'], ['L4', 'L41', 'others', 'word_characters', '2', '1', 'E04'], ['L4', 'L42', 'others', 'digits', '6', '6', 'E02'], ['NEW', 'SECTION']])

    def test_getErrorCode(self):
        try:
            error_template = input_file_parser.getErrorCode(error_code_file)
        except Exception as Ex:
            input_file_parser.log_error(str(Ex)+'\n')
        finally:
            self.assertEqual(error_template, ['LXY field under segment LX passes all the validation criteria.', 'LXY field under section LX fails the data type (expected: {data_type}) validation, however it passes the max length ({max_length}) validation', 'LXY field under section LX fails the max length (expected: {max_length}) validation, however it passes the data type ({data_type}) validation', 'LXY field under section LX fails all the validation criteria.', 'LXY field under section LX is missing.'])

    def test_writeReport(self):
        try:
            input_value = input_file_parser.getInputData(input_file)
            standard_def = input_file_parser.getStandardDef(standard_def_file)
            concluded_value = input_file_parser.checkValidation(input_value, standard_def)
        except Exception as Ex:
            input_file_parser.log_error(str(Ex)+'\n')
        finally:
            self.assertEqual(input_file_parser.writeReport(concluded_value), True)

    def test_writeSummary(self):
        try:
            input_value = input_file_parser.getInputData(input_file)
            standard_def = input_file_parser.getStandardDef(standard_def_file)
            concluded_value = input_file_parser.checkValidation(input_value, standard_def)
            error_template = input_file_parser.getErrorCode(error_code_file)
        except Exception as Ex:
            input_file_parser.log_error(str(Ex)+'\n')
        finally:
            self.assertEqual(input_file_parser.writeSummary(concluded_value, error_template), True)

if __name__=='__main__':
        
    input_file = input("Enter input file name: ")
    standard_def_file = input("Enter standard definition file name: ")
    error_code_file = input("Enter error code file name: ")

    unittest.main()