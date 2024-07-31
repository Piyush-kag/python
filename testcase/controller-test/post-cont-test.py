import unittest
from unittest.mock import MagicMock, patch, Mock
import requests
from loguru import logger


def get_post_data_by_id(post_id):
    response = requests.get(f"http://localhost:8000/posts/{post_id}")
    return response.json()


def add_post_data():
    post_data = {
        "id": 5,
        "title": "title is here",
        "content": "content is here.",
        "user_id": 1
    }
    response = requests.post("http://localhost:8000/posts", json=post_data)
    return response.json()


class TestPostDetails(unittest.TestCase):

    @patch("requests.get")
    def test_post_data(self, mock_get):
        mock_response_post = Mock()
        response_dict_post = {
            "id": 1,
            "title": "title",
            "user_id": 1,
            "content": "content"
        }
        mock_response_post.json.return_value = response_dict_post
        mock_response_post.status_code = 200
        mock_get.return_value = mock_response_post

        post_data = get_post_data_by_id(1)

        mock_get.assert_called_with("http://localhost:8000/posts/1")
        self.assertEqual(mock_response_post.status_code, 200)
        self.assertEqual(post_data, response_dict_post)
        logger.success("Passed - Test Case to get post data.")

    @patch("requests.post")
    def test_add_post(self, mock_add_post):
        mock_response_post = Mock()
        response_dict_add_post = {
            "id": 5,
            "title": "title is here",
            "user_id": 1,
            "content": "content is here."
        }
        mock_response_post.json.return_value = response_dict_add_post
        mock_response_post.status_code = 201
        mock_add_post.return_value = mock_response_post

        post_data = add_post_data()

        mock_add_post.assert_called_with(
            "http://localhost:8000/posts",
            json={
                "id": 5,
                "title": "title is here",
                "user_id": 1,
                "content": "content is here."
            }
        )
        self.assertEqual(mock_response_post.status_code, 201)
        self.assertEqual(post_data, response_dict_add_post)
        logger.success("Passed - Test Case to add post.")


if __name__ == '__main__':
    unittest.main()
