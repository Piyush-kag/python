import unittest
from unittest.mock import patch, Mock
import requests
from loguru import logger


def get_all_employee_by_id_test(employee_id):
    response = requests.get(f"http://localhost:8000/employees/{employee_id}")
    return response.json()


def add_employee_data():
    employee_data = {
        "name": "Piyush Kag",
        "address": "123 Street",
        "phone_number": "1234567890"
    }
    response = requests.post("http://localhost:8000/employees", json=employee_data)
    return response.json()


def update_employee_data(employee_id, name=None, address=None, phone_number=None):
    employee_data = {
        "name": name,
        "address": address,
        "phone_number": phone_number
    }
    response = requests.put(f"http://localhost:8000/employees/{employee_id}", json=employee_data)
    return response.json()


def delete_employee_data(employee_id):
    response = requests.delete(f"http://localhost:8000/employees/{employee_id}")
    return response.json(), response.status_code


class TestEmployeeDetails(unittest.TestCase):

    @patch("requests.get")
    def test_employee_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "id": 1,
            "name": "Piyush Kag",
            "details": {
                "id": 1,
                "employee_id": 1,
                "address": "123 Street",
                "phone_number": "1234567890"
            }
        }
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        emp_data = get_all_employee_by_id_test(1)

        mock_get.assert_called_with("http://localhost:8000/employees/1")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(emp_data, response_dict)
        logger.success("Passed - Test Case to get employee data.")

    @patch("requests.get")
    def test_employee_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "Employee with id 1 not found"}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        emp_data = get_all_employee_by_id_test(1)

        mock_get.assert_called_with("http://localhost:8000/employees/1")
        self.assertEqual(mock_response.status_code, 404)
        self.assertEqual(emp_data, {"detail": "Employee with id 1 not found"})
        logger.success("Passed - Test Case for employee not found.")

    @patch("requests.post")
    def test_add_employee(self, mock_post):
        mock_response_post = Mock()
        response_dict_add_employee = {
            "id": 4,
            "name": "Piyush Kag",
            "details": {
                "id": 4,
                "employee_id": 4,
                "address": "123 Street",
                "phone_number": "1234567890"
            }
        }
        mock_response_post.json.return_value = response_dict_add_employee
        mock_response_post.status_code = 201
        mock_post.return_value = mock_response_post

        employee_data = add_employee_data()

        mock_post.assert_called_with(
            "http://localhost:8000/employees",
            json={
                "name": "Piyush Kag",
                "address": "123 Street",
                "phone_number": "1234567890"
            }
        )
        self.assertEqual(mock_response_post.status_code, 201)
        self.assertEqual(employee_data, response_dict_add_employee)
        logger.success("Passed - Test Case to add employee.")

    @patch("requests.post")
    def test_add_employee_failure(self, mock_post):
        mock_response_post = Mock()
        mock_response_post.json.return_value = {"detail": "An error occurred while creating the employee"}
        mock_response_post.status_code = 400
        mock_post.return_value = mock_response_post

        employee_data = add_employee_data()

        mock_post.assert_called_with(
            "http://localhost:8000/employees",
            json={
                "name": "Piyush Kag",
                "address": "123 Street",
                "phone_number": "1234567890"
            }
        )
        self.assertEqual(mock_response_post.status_code, 400)
        self.assertEqual(employee_data, {"detail": "An error occurred while creating the employee"})
        logger.success("Passed - Test Case for add employee failure.")

    @patch("requests.put")
    def test_update_employee(self, mock_put):
        mock_response_put = Mock()
        response_dict_update_employee = {
            "id": 1,
            "name": "Piyush Kag Updated",
            "details": {
                "id": 1,
                "employee_id": 1,
                "address": "456 Avenue",
                "phone_number": "9876543210"
            }
        }
        mock_response_put.json.return_value = response_dict_update_employee
        mock_response_put.status_code = 200
        mock_put.return_value = mock_response_put

        employee_data = update_employee_data(1, "Piyush Kag Updated", "456 Avenue", "9876543210")

        mock_put.assert_called_with(
            "http://localhost:8000/employees/1",
            json={
                "name": "Piyush Kag Updated",
                "address": "456 Avenue",
                "phone_number": "9876543210"
            }
        )
        self.assertEqual(mock_response_put.status_code, 200)
        self.assertEqual(employee_data, response_dict_update_employee)
        logger.success("Passed - Test Case to update employee.")

    @patch("requests.put")
    def test_update_employee_not_found(self, mock_put):
        mock_response_put = Mock()
        mock_response_put.json.return_value = {"detail": "Employee with id 1 not found"}
        mock_response_put.status_code = 404
        mock_put.return_value = mock_response_put

        employee_data = update_employee_data(1, "Piyush Kag Updated", "456 Avenue", "9876543210")

        mock_put.assert_called_with(
            "http://localhost:8000/employees/1",
            json={
                "name": "Piyush Kag Updated",
                "address": "456 Avenue",
                "phone_number": "9876543210"
            }
        )
        self.assertEqual(mock_response_put.status_code, 404)
        self.assertEqual(employee_data, {"detail": "Employee with id 1 not found"})
        logger.success("Passed - Test Case for update employee not found.")

    @patch("requests.delete")
    def test_delete_employee(self, mock_delete):
        mock_response_delete = Mock()
        mock_response_delete.json.return_value = {"detail": "Employee deleted"}
        mock_response_delete.status_code = 200
        mock_delete.return_value = mock_response_delete

        response_data, status_code = delete_employee_data(1)

        mock_delete.assert_called_with("http://localhost:8000/employees/1")
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data, {"detail": "Employee deleted"})
        logger.success("Passed - Test Case to delete employee.")

    @patch("requests.delete")
    def test_delete_employee_not_found(self, mock_delete):
        mock_response_delete = Mock()
        mock_response_delete.json.return_value = {"detail": "Employee with id 1 not found"}
        mock_response_delete.status_code = 404
        mock_delete.return_value = mock_response_delete

        response_data, status_code = delete_employee_data(1)

        mock_delete.assert_called_with("http://localhost:8000/employees/1")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data, {"detail": "Employee with id 1 not found"})
        logger.success("Passed - Test Case for delete employee not found.")


if __name__ == '__main__':
    unittest.main()
