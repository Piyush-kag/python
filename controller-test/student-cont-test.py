import unittest
from unittest.mock import MagicMock, patch, Mock
import requests
from loguru import logger


def get_all_students_test():
    response = requests.get(f"http://localhost:8000/students")
    return response.json()


def add_student_data():
    student_data = {
        "id": 4,
        "student_name": "pk",
        "courses": []
    }
    response = requests.post("http://localhost:8000/students", json=student_data)
    return response.json()


class TestStudentDetails(unittest.TestCase):

    @patch("requests.get")
    def test_student_data(self, mock_get):
        mock_response = Mock()
        response_dict = [
            {
                "id": 0,
                "student_name": "string",
                "courses": []
            }
        ]
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        std_data = get_all_students_test()

        mock_get.assert_called_with("http://localhost:8000/students")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(std_data, response_dict)
        logger.success("Passed - Test Case to get student data.")

    @patch("requests.post")
    def test_add_student(self, mock_post):
        mock_response_post = Mock()
        response_dict_add_student = {
            "id": 4,
            "student_name": "pk",
            "courses": []
        }
        mock_response_post.json.return_value = response_dict_add_student
        mock_response_post.status_code = 201
        mock_post.return_value = mock_response_post

        user_data = add_student_data()

        mock_post.assert_called_with(
            "http://localhost:8000/students",
            json={
                "id": 4,
                "student_name": "pk",
                "courses": []
            }
        )
        self.assertEqual(mock_response_post.status_code, 201)
        self.assertEqual(user_data, response_dict_add_student)
        logger.success("Passed - Test Case to add student.")


if __name__ == '__main__':
    unittest.main()
