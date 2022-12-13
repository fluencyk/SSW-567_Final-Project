from MRTD import MRTD
import json


def main():
    document_reader = MRTD()
    
    ## DECODE A STRING
    #print(document_reader.decode('P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'))

    ## TEST ALL CHECK VALUES
    
    #print(document_reader.decode('P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'))
    result = document_reader.decode('P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6')
    print(result == json.dumps({
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
        }))
    ## ENCODE A STRING
    # print (document_reader.encode(
    # {
    #         "line1": {
    #             "issuing_country": "CIV",
    #             "last_name": "LYNN",
    #             "given_name": "NEVEAH BRAM"
    #         },
    #         "line2": {
    #             "passport_number": "W620126G5",
    #             "country_code": "CIV",
    #             "birth_date": "591010",
    #             "sex": "F",
    #             "expiration_date": "970730",
    #             "personal_number": "AJ010215I"
    #         }
    #     }    
    # ) == 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6')
    
    
    
if __name__ == "__main__":
    main()
