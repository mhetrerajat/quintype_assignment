"""
    This module invloves test cases for api. Run this test cases in development
    environment. To run test cases, type command in terminal :
    >> python3 test.py
"""
import unittest
import json

from app import app


class TestCase(unittest.TestCase):
    """
        TestCase class inherits from unittest.TestCase
    """

    def test_add_car_case_one(self):
        """
            Add Car : Case One
            Expected Outcome:
                Data should be added into database by passing all validation cases
                and expected result should same as mentioned in following method.
        """
        tester = app.test_client(self)
        params = {
            'latitude': 22.22,
            'longitude': 22.22,
            'is_pink': False
        }
        expected_result = {
            'result': {
                'latitude': 22.22,
                'longitude': 22.22,
                'is_pink': False
            }
        }
        response = tester.post('/car', data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(
                response.data.decode('utf-8')),
            expected_result)

    def test_add_car_case_two(self):
        """
            Add Car : Case Two
            Expected Outcome:
                Validation error should be given as latitude cannot be string,
                it must be float. Response should match with following expected
                output.
        """
        tester = app.test_client(self)
        params = {
            'latitude': "asd",
            'longitude': 22.22,
            'is_pink': False
        }
        expected_result = {
            'result': 'Please provide valid latitude/longitude.'
        }
        response = tester.post('/car', data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(
                response.data.decode('utf-8')),
            expected_result)

    def test_add_car_case_three(self):
        """
            Add Car : Case Three
            Expected Outcome:
                Validation error should be given as required params
                are missing. Response should match with following expected
                output.
        """
        tester = app.test_client(self)
        params = {
            'latitude': "",
            'longitude': 22.22,
            'is_pink': False
        }
        expected_result = {
            'result': 'Please provide valid latitude/longitude.'
        }
        response = tester.post('/car', data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(
                response.data.decode('utf-8')),
            expected_result)

    def test_finish_book_case_one(self):
        """
            Finish Book : Case One
            Expected Outcome:
                Valid data is provided so car should be booked.
                Result should match with expected output mention in following
                method.
        """
        tester = app.test_client(self)
        customer_id = 1
        request_url = '/customer/' + str(customer_id) + '/complete'
        params = {
            'latitude': 22.22,
            'longitude': 22.22
        }
        expected_result = {
            'result': 'Journey completed successfully.'
        }
        response = tester.post(request_url, data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(
                response.data.decode('utf-8')),
            expected_result)

    def test_finish_book_case_two(self):
        """
            Finish Book : Case Two
            Expected Outcome:
                Invalid customer_id is given i.e. random id is given as
                parameter and database don't have any customer record associated
                with that id.
        """
        tester = app.test_client(self)
        customer_id = 99999999999
        request_url = '/customer/' + str(customer_id) + '/complete'
        params = {
            'latitude': 22.22,
            'longitude': 22.22
        }
        expected_result = {
            'result': 'Oops! Customer with given id does not exists. Please check customer_id.'
        }
        response = tester.post(request_url, data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(
                response.data.decode('utf-8')),
            expected_result)

    def test_book_car_case_one(self):
        """
            Book Car : Case One
            Expected Outcome:
                Valid data is provided as parameter so booking should be
                done succesfully. Response status_code should be 201.
        """
        tester = app.test_client(self)
        params = {
            'latitude': 22.22,
            'longitude': 22.22,
            'is_pink': True
        }
        expected_result = {
            "result": [
                {
                    "available_status": False,
                    "id": 1,
                    "is_pink": True,
                    "latitude": 22.22,
                    "longitude": 22.22
                },
                {
                    "available_status": True,
                    "id": 4,
                    "is_pink": True,
                    "latitude": 44.33,
                    "longitude": 33.22
                }
            ]
        }
        response = tester.post('/customer/book', data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(
                response.data.decode('utf-8')),
            expected_result)

if __name__ == '__main__':
    unittest.main()
