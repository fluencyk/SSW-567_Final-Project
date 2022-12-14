# -*- coding: utf-8 -*-
"""
@author: yujun kong
implemented: Dec. 12, 2022
This script creates a testing to review the performance of the main program and unit tests
"""

import sys, json, time, csv
import matplotlib.pyplot as plt
from typing import IO
from MRTD import MRTD
from MTTDtest import TestMRTD

class Perf_Test:

    # base constructor
    def __init__(self) -> None:
        
        self.json_data: dict = {}

    """/* support methods */"""
    def open_file(self, file_name: str) -> IO:

        while True:
            try:
                gotten_File: IO = open(file_name, 'r', encoding = 'gbk', errors = 'ignore')
                return gotten_File
            except FileNotFoundError:
                print("The file name is invalid or the file does not exist, program ends!")
                sys.exit()

    def get_json_file_data(self, json_file: IO) -> None:

        with json_file as curr_json:
            self.json_data = json.load(curr_json)

    """/* core methods */"""
    def process_perf_count_lines(self, file_name: str, restricted_lines_number: int) -> int:

        response_time_result: str

        count: int = 0
        open_point = time.perf_counter()
        for line in enumerate(self.open_file(file_name)):
            count += 1
            if count == restricted_lines_number:
                break
        close_point = time.perf_counter()
        # print(count) #<- manual test
        response_time_result = str("%.4f" %(close_point - open_point))
        # print(f"Cost {response_time_result} Seconds to read {restricted_lines_number} lines from file '{file_name}'\n") #<- manual test
        return response_time_result

    def process_perf_test_self(self, process_option: str, execution_times: int, is_with_unittest: bool) -> str:
        
        conditional_words: str
        mrtd = MRTD()
        unit_test = TestMRTD()
        count: int = 0
        response_time_result: str

        if process_option == 'decode':
            self.get_json_file_data(self.open_file('records_encoded.json'))
            i: dict
            request_point = time.perf_counter()
            for i in self.json_data['records_encoded']:
                    mrtd.decode(i)
                    if is_with_unittest == False:
                        conditional_words = ''
                    else:
                        conditional_words = '(with unit tests assertions in place)'
                        unit_test.test_decode()
                    count += 1
                    if count == execution_times:
                        break                    
            response_point = time.perf_counter()
            response_time_result = str("%.4f" %(response_point - request_point))
            # print(f"Consumed {response_time_result} Seconds to process all decoding data {conditional_words}\n") #<- manual test
            return response_time_result

        if process_option == 'encode':
            self.get_json_file_data(self.open_file('records_decoded.json'))
            j: dict
            start_point = time.perf_counter()
            for j in self.json_data['records_decoded']:
                    mrtd.encode(j)
                    if is_with_unittest == False:
                        conditional_words = ''
                    else:
                        conditional_words = '(with unit tests assertions in place)'
                        unit_test.test_encode()
                    count += 1
                    if count == execution_times:
                        break
            end_point = time.perf_counter()
            response_time_result = str("%.4f" %(end_point - start_point))
            # print(f"Consumed {response_time_result} Seconds to process all encoding data {conditional_words}\n") #<- manual test
            return response_time_result

    def output_csv_file(self) -> None:

        with open('perf_test_records.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(['#', 'Response Time Scales', 'Decoding Number of Lines', 'Encoding Number of Lines', 'Decoding without Tests', 'Decoding with Unit Tests', 'Encoding without Tests', 'Encoding with Unit Tests'])
            writer.writerows([
                ['01', 'Seconds in 100 units', self.process_perf_count_lines('records_decoded.json', 100), self.process_perf_count_lines('records_encoded.json', 100), self.process_perf_test_self('decode', 100, False), self.process_perf_test_self('decode', 100, True), self.process_perf_test_self('encode', 100, False), self.process_perf_test_self('encode', 100, True)],
                ['02', 'Seconds in 500 units', self.process_perf_count_lines('records_decoded.json', 500), self.process_perf_count_lines('records_encoded.json', 500), self.process_perf_test_self('decode', 500, False), self.process_perf_test_self('decode', 500, True), self.process_perf_test_self('encode', 500, False), self.process_perf_test_self('encode', 500, True)],
                ['03', 'Seconds in 1000 units', self.process_perf_count_lines('records_decoded.json', 1000), self.process_perf_count_lines('records_encoded.json', 1000), self.process_perf_test_self('decode', 1000, False), self.process_perf_test_self('decode', 1000, True), self.process_perf_test_self('encode', 1000, False), self.process_perf_test_self('encode', 1000, True)],
                ['04', 'Seconds in 5000 units', self.process_perf_count_lines('records_decoded.json', 5000), self.process_perf_count_lines('records_encoded.json', 5000), self.process_perf_test_self('decode', 5000, False), self.process_perf_test_self('decode', 5000, True), self.process_perf_test_self('encode', 5000, False), self.process_perf_test_self('encode', 5000, True)],
                ['05', 'Seconds in 10000 units', self.process_perf_count_lines('records_decoded.json', 10000), self.process_perf_count_lines('records_encoded.json', 10000), self.process_perf_test_self('decode', 10000, False), self.process_perf_test_self('decode', 10000, True), self.process_perf_test_self('encode', 10000, False), self.process_perf_test_self('encode', 10000, True)],
                ['06', 'Seconds in specific units', self.process_perf_count_lines('records_decoded.json', 150004), self.process_perf_count_lines('records_encoded.json', 10004)]
            ])

    def plot_response_time_record(self) -> None:

        x = [100, 500, 1000, 5000, 10000, 50000, 100000]

        de_cnt_lns = [
            self.process_perf_count_lines('records_decoded.json', 100),
            self.process_perf_count_lines('records_decoded.json', 500),
            self.process_perf_count_lines('records_decoded.json', 1000),
            self.process_perf_count_lines('records_decoded.json', 5000),
            self.process_perf_count_lines('records_decoded.json', 10000),
            self.process_perf_count_lines('records_decoded.json', 50000),
            self.process_perf_count_lines('records_decoded.json', 100000)
        ]

        en_cnt_lns = [
            self.process_perf_count_lines('records_encoded.json', 100),
            self.process_perf_count_lines('records_encoded.json', 500),
            self.process_perf_count_lines('records_encoded.json', 1000),
            self.process_perf_count_lines('records_encoded.json', 5000),
            self.process_perf_count_lines('records_encoded.json', 10000),
            self.process_perf_count_lines('records_encoded.json', 50000),
            self.process_perf_count_lines('records_encoded.json', 100000)
        ]

        decode_without_test = [
            self.process_perf_test_self('decode', 100, False),
            self.process_perf_test_self('decode', 500, False),
            self.process_perf_test_self('decode', 1000, False),
            self.process_perf_test_self('decode', 5000, False),
            self.process_perf_test_self('decode', 10000, False),
            self.process_perf_test_self('decode', 50000, False),
            self.process_perf_test_self('decode', 100000, False)
        ]

        decode_with_test = [
            self.process_perf_test_self('decode', 100, True),
            self.process_perf_test_self('decode', 500, True),
            self.process_perf_test_self('decode', 1000, True),
            self.process_perf_test_self('decode', 5000, True),
            self.process_perf_test_self('decode', 10000, True),
            self.process_perf_test_self('decode', 50000, True),
            self.process_perf_test_self('decode', 100000, True),
        ]

        encode_without_test = [
            self.process_perf_test_self('encode', 100, False),
            self.process_perf_test_self('encode', 500, False),
            self.process_perf_test_self('encode', 1000, False),
            self.process_perf_test_self('encode', 5000, False),
            self.process_perf_test_self('encode', 10000, False),
            self.process_perf_test_self('encode', 50000, False),
            self.process_perf_test_self('encode', 100000, False)
        ]

        encode_with_test = [
            self.process_perf_test_self('encode', 100, True),
            self.process_perf_test_self('encode', 500, True),
            self.process_perf_test_self('encode', 1000, True),
            self.process_perf_test_self('encode', 5000, True),
            self.process_perf_test_self('encode', 10000, True),
            self.process_perf_test_self('encode', 50000, True),
            self.process_perf_test_self('encode', 100000, True)
        ]

        plt.plot(x, de_cnt_lns, marker = 's', c = 'gold', label = 'Decoding Number of Lines')
        plt.plot(x, en_cnt_lns, marker = 'o', c = 'darkorange', label = 'Encoding Number of Lines')

        plt.plot(x, decode_without_test, marker = '^', c = 'r', label = 'Decoding')
        plt.plot(x, decode_with_test, marker = 'v', c = 'm', label = 'Decoding with Tests')

        plt.plot(x, encode_without_test, marker = '+', c = 'lime', label = 'Encoding')
        plt.plot(x, encode_with_test, marker = 'X', c = 'aqua', label = 'Encoding with Tests')

        plt.xlabel('Processed Units (Per Lines / Record)')
        plt.ylabel('Response Time (Seconds)')

        plt.legend(loc = 'best')
        plt.show()

def main():

    curr_perf_test = Perf_Test()

    curr_perf_test.output_csv_file()
    curr_perf_test.plot_response_time_record()

    sys.exit()

if __name__ == "__main__":
    main()
