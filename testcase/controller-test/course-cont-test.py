import unittest
from unittest.mock import MagicMock, patch, Mock
import requests
from loguru import logger


def get_all_course_test():
    response = requests.get(f"http://localhost:8000/course")
    return response.json()


def add_course_data():
    course_data = {
        "student_name": "pk",
    }
    response = requests.post("http://localhost:8000/students", json=course_data)
    return response.json()


class TestCourseDetails(unittest.TestCase):

    @patch("requests.get")
    def test_course_data(self, mock_get):
        mock_response = Mock()
        response_dict = [
            {
                "id": 0,
                "course_name": "string",
                "student_count": 0
            }
        ]
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        course_data = get_all_course_test()

        mock_get.assert_called_with("http://localhost:8000/course")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(course_data, response_dict)
        logger.success("Passed - Test Case to get course data.")

    @patch("requests.post")
    def test_add_student(self, mock_post):
        mock_response_post = Mock()
        response_dict_add_student = {
            "id": 0,
            "course_name": "string",
            "student_count": 0
        }
        mock_response_post.json.return_value = response_dict_add_student
        mock_response_post.status_code = 201
        mock_post.return_value = mock_response_post

        course_data = add_course_data()

        mock_post.assert_called_with(
            "http://localhost:8000/students",
            json={
                "student_name": "pk"
            }
        )
        self.assertEqual(mock_response_post.status_code, 201)
        self.assertEqual(course_data, response_dict_add_student)
        logger.success("Passed - Test Case to add course.")


if __name__ == '__main__':
    unittest.main()
