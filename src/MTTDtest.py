# -*- coding: utf-8 -*-
"""
@author: carmen couzyn
year: 2022
This script tests the functions implemented in MRTD.py
"""

import unittest
from unittest.mock import patch
from MRTD import MRTD
import json


class TestMRTD(unittest.TestCase):
  
  ## TESTS FOR THE MAIN FUNCTIONS

    """ Testing empty scan function. 
        Included to improve code coverage.
    """
    def test_scan(self):
        mrtd = MRTD()
        self.assertEqual(mrtd.scan(), '')

    """ Testing empty load_data_from_db function. 
        Included to improve code coverage.
    """
    def test_load_data_from_db(self):
        mrtd = MRTD()
        self.assertEqual(mrtd.load_data_from_db(), '')


    """ Testing the decode function with a valid input:
            The aim of this test is to assert that a encoded string
            will be correctly decoded into document fields
    """    
    @patch.object(MRTD, 'scan')
    def test_decode(self,  mock_scan):

        mrtd = MRTD()

        mock_scan.return_value = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'


        self.assertEqual(json.dumps({
            "line1": {
                "issuing_country": "CIV",
                "last_name": "LYNN",
                "given_name": "NEVEAH BRAM"
            },
            "line2": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "AJ010215I"
            }
        }), mrtd.decode(mock_scan()))
    
    
    """ Testing the encode function with a valid input:
            The aim of this test is to assert that a document object
            will be correctly encoded into the machine readable string
    """    
    @patch.object(MRTD, 'load_data_from_db')
    def test_encode(self, mock_load_data_from_db):
          
        mrtd = MRTD()

        mock_load_data_from_db.return_value = {
            "line1": {
                "issuing_country": "REU",
                "last_name": "MCFARLAND",
                "given_name": "TRINITY AMITY"
            },
            "line2": {
                "passport_number": "Q683170H1",
                "country_code": "REU",
                "birth_date": "640313",
                "sex": "M",
                "expiration_date": "690413",
                "personal_number": "UK128819I"
            }
        }

        expected_result = "P<REUMCFARLAND<<TRINITY<AMITY<<<<<<<<<<<<<<<;Q683170H11REU6403131M6904133UK128819I<<<<<<9"
        result = mrtd.encode(mock_load_data_from_db())
                
        self.assertEqual(result , expected_result)
        

    # Test control digit check function
    # takes encoded string and returns string indicating an error including field information or a pass   

    """ Testing the control_check_digits function with valid input
            The aim of this test is to assert that correct check digits
            will be recognized
    """    
    @patch.object(MRTD, 'scan')
    def test_control_check_digits_valid(self, mock_scan):
        mrtd = MRTD()

        mock_scan.return_value = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'

        expected_result = 'All check digit passed'
        result = mrtd.control_check_digits(mock_scan())
                
        self.assertEqual(result , expected_result)
        

    """ Testing the control_check_digits function with invalid input at passport_number
            The aim of this test is to assert that an incorrect check digit
            will be recognized and the correct field will be flagged
    """    
    @patch.object(MRTD, 'scan')
    def test_control_check_digit_invalid_password_number(self, mock_scan):
        mrtd = MRTD()

        mock_scan.return_value = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G52CIV5910106F9707302AJ010215I<<<<<<6'

        expected_result = 'Error: False check digit at passport_number'
        result = mrtd.control_check_digits(mock_scan())
                
        self.assertEqual(result , expected_result)

    """ Testing the control_check_digits function with invalid input at birth_date
            The aim of this test is to assert that an incorrect check digit
            will be recognized and the correct field will be flagged
    """    
    @patch.object(MRTD, 'scan')
    def test_control_check_digit_invalid_birth_date(self, mock_scan):
        mrtd = MRTD()

        mock_scan.return_value = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910103F9707302AJ010215I<<<<<<6'

        expected_result = 'Error: False check digit at birth_date'
        result = mrtd.control_check_digits(mock_scan())
                
        self.assertEqual(result , expected_result)

    """ Testing the control_check_digits function with invalid input at expiration_date
            The aim of this test is to assert that an incorrect check digit
            will be recognized and the correct field will be flagged
    """    
    @patch.object(MRTD, 'scan')
    def test_control_check_digit_invalid_expiration_date(self, mock_scan):
        mrtd = MRTD()

        mock_scan.return_value = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707308AJ010215I<<<<<<6'

        expected_result = 'Error: False check digit at expiration_date'
        result = mrtd.control_check_digits(mock_scan())
                
        self.assertEqual(result , expected_result)

    """ Testing the control_check_digits function with invalid input at personal_number
            The aim of this test is to assert that an incorrect check digit
            will be recognized and the correct field will be flagged
    """    
    @patch.object(MRTD, 'scan')
    def test_control_check_digit_invalid_personal_number(self, mock_scan):
        mrtd = MRTD()

        mock_scan.return_value = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<9'

        expected_result = 'Error: False check digit at personal_number'
        result = mrtd.control_check_digits(mock_scan())
                
        self.assertEqual(result , expected_result)


    ## TESTS FOR THE HELPER FUNCTION

    """ Testing the get_check_digits function with all uppercase letters
    """    
    def test_get_check_digit(self):
        mrtd = MRTD()

        expected_result = 6
        result = mrtd.get_check_digit('L898902C3')

        self.assertEqual(result , expected_result)


    """ Testing the get_check_digits function with all lowercase letters
    """    
    def test_get_check_digit_lowercase(self):
        mrtd = MRTD()

        expected_result = 6
        result = mrtd.get_check_digit('l898902c3')

        self.assertEqual(result , expected_result)



    """ Testing the get_check_digits function with symbols
    """    
    def test_get_check_digit_symbol(self):
        mrtd = MRTD()

        expected_result = 1
        result = mrtd.get_check_digit('ZE184226B<<<<<<')

        self.assertEqual(result , expected_result)




if __name__ == '__main__':
    unittest.main()