# -*- coding: utf-8 -*-
"""
@author: carmen couzyn
year: 2022
This script creates functions for the scan and 
decoding of machine-readable travel documents
"""

from base64 import encode
import re
import json

    
class MRTD:
    
    """ Testing empty scan function:
        Mocking hardware implementation
    """
    def scan(self):
        return ''

    """ Testing empty load_data function:
        Mocking database connection
    """
    def load_data_from_db(self):
        return ''
    
    """ Decode function:
        args: an encoded machine-readable string, format: 'line1;line2' 
        returns: decoded document fields as json
    """
    def decode(self, encoded_document_string):

        lines_arr = encoded_document_string.split(';')
        
        string1 = lines_arr[0]
        string2 = lines_arr[1]
        
        full_name = string1[5:len(string1)].replace('<', ' ')
        names = full_name.split()
        last_name = names[0]
        names.pop(0)
        given_name = " ".join(names)
        
        return_str = {
            "line1": {
                "issuing_country": string1[2:5],
                "last_name": last_name,
                "given_name": given_name
                } ,
            "line2": {
                    "passport_number": string2[0:9],
                    "country_code": string2[10:13],
                    "birth_date": string2[13:19],
                    "sex": string2[20],
                    "expiration_date": string2[21:27],
                    "personal_number": string2[28:37]
                }
        }
        return json.dumps(return_str)
        
    
    
    
    """ Encode function:
        args: document fields as json 
        returns: encoded machine-readable string
    """
    def encode(self, document):
        
        line1 = document['line1']
        line2 = document['line2']

        
        # Line 1
        string1 = 'P<' + line2['country_code'] + line1['last_name'] + '<<' + line1['given_name'].replace(' ', '<')
        total_string_length = 44
        for x in range(total_string_length - len(string1)):
           string1 += '<'
        
        # Line 2
        string2 = line2['passport_number'] + str(self.get_check_digit(line2['passport_number'])) + line2['country_code'] + line2['birth_date'] + str(self.get_check_digit(line2['birth_date'])) + line2['sex'] + line2['expiration_date'] + str(self.get_check_digit(line2['expiration_date'])) + line2['personal_number'] + '<<<<<<' + str(self.get_check_digit(line2['personal_number']))
        
        return string1 + ';' + string2
        
 
 
    """ Control check digits function:
        Checks if all check digits have the correct value.
        args: encoded machine-readable string
        returns: success --> 'All check digits passed' 
                 error --> 'Error: False check digit at <field_name>'
    """
    def control_check_digits(self, encoded_document_string):
        fields_to_check = [{
            'field_name': 'passport_number',
            'check_digit_index': 9
        },
        {
            'field_name': 'birth_date',
            'check_digit_index': 19
        },
        {
            'field_name': 'expiration_date',
            'check_digit_index': 27
        },
        {
            'field_name': 'personal_number',
            'check_digit_index': 43
        }]
        
        
        decoded_document = json.loads(self.decode(encoded_document_string))
    
        line2_decoded = decoded_document['line2']
        line2_encoded = encoded_document_string.split(';')[1]
        
                         
        for field in fields_to_check:
            document_field_value = line2_decoded[field['field_name']]
            calculated_check_digit = self.get_check_digit(document_field_value)
            index = field['check_digit_index']
            document_check_digit = line2_encoded[index]
            if document_check_digit != str(calculated_check_digit): 
                return 'Error: False check digit at {}'.format(field['field_name'])
        
        return 'All check digit passed'

    
    
    # Helper function
    """ Get check digit function:
        This is a helper function that takes a string and calculates the check digit.
        args: encoded string of a docoument field
        returnd: check digit as int
    """
    def get_check_digit(self, encoded_string):

        # initialize check digit to 0
        check_digit = 0
        weighting_sequence = [7, 3, 1]

        for index, character in enumerate(encoded_string):
            ## Encode each character depending on their char value compared to a or A

            #lower_case letters
            if re.search('[a-z]', character):
                encoded_character = (ord(character)-ord('a') + 10) 
            
            # upper_case_letters
            elif re.search('[A-Z]', character):
                encoded_character = (ord(character)-ord('A') + 10) 
            
            # digits
            elif re.search('[0-9]', character):
                encoded_character = int(character)

            # symbols
            elif re.search("[$&+,:;=?@#|'<>.-^*()%!]", character):
                  encoded_character = 0

            # Weigh the encoded character
            weighted_c = int(encoded_character) * weighting_sequence[index % len(weighting_sequence)]

            # add the weighted character to the check digit
            check_digit += weighted_c

        check_digit = check_digit % 10
        return check_digit
