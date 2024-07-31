import unittest
from unittest.mock import patch, Mock
import requests
from loguru import logger


def get_user_data_by_id(user_id):
    response = requests.get(f"http://localhost:8000/users/{user_id}")
    return response.json()


def add_user_data():
    user_data = {
        "username": "piyush1",
        "email": "piyushkag11@gmail.com",
        "model_computed_fields": "some_computed_field",
        "posts": []
    }
    response = requests.post("http://localhost:8000/users", json=user_data)
    return response.json()


def delete_user_by_id(user_id):
    response = requests.delete(f"http://localhost:8000/users/{user_id}")
    return response.json()


def fetch_users_from_tp_api():
    response = requests.post("http://localhost:8000/fetch-users-from-tp-api")
    return response.json()


def get_all_users():
    response = requests.get("http://localhost:8000/users/")
    return response.json()


def get_user_by_word(word):
    response = requests.get(f"http://localhost:8000/byword/{word}")
    return response.json()


def get_paginated_users(limit):
    response = requests.get(f"http://localhost:8000/paginated-users/?limit={limit}")
    return response.json()


# Test cases
class TestUserDetails(unittest.TestCase):

    @patch("requests.get")
    def test_user_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "username": "pk",
            "email": "pk@gmail.com",
            "id": 1
        }
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        user_data = get_user_data_by_id(1)

        mock_get.assert_called_with("http://localhost:8000/users/1")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(user_data, response_dict)
        logger.success("Passed - Test Case to get user data.")

    @patch("requests.get")
    def test_user_data_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "User not found."}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        user_data = get_user_data_by_id(999)

        mock_get.assert_called_with("http://localhost:8000/users/999")
        self.assertEqual(mock_response.status_code, 404)
        self.assertEqual(user_data, {"detail": "User not found."})
        logger.success("Passed - Test Case to get user data not found.")

    @patch("requests.get")
    def test_user_data_internal_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "Internal Server Error"}
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        user_data = get_user_data_by_id(1)

        mock_get.assert_called_with("http://localhost:8000/users/1")
        self.assertEqual(mock_response.status_code, 500)
        self.assertEqual(user_data, {"detail": "Internal Server Error"})
        logger.success("Passed - Test Case to handle internal server error for user data.")

    @patch("requests.post")
    def test_add_user(self, mock_post):
        mock_response_post = Mock()
        response_dict_add_user = {
            "id": 14,
            "username": "piyush1",
            "email": "piyushkag11@gmail.com",
            "model_computed_fields": "some_computed_field",
            "posts": []
        }
        mock_response_post.json.return_value = response_dict_add_user
        mock_response_post.status_code = 201
        mock_post.return_value = mock_response_post

        user_data = add_user_data()

        mock_post.assert_called_with(
            "http://localhost:8000/users",
            json={
                "username": "piyush1",
                "email": "piyushkag11@gmail.com",
                "model_computed_fields": "some_computed_field",
                "posts": []
            }
        )
        self.assertEqual(mock_response_post.status_code, 201)
        self.assertEqual(user_data, response_dict_add_user)
        logger.success("Passed - Test Case to add user.")

    @patch("requests.post")
    def test_add_user_internal_server_error(self, mock_post):
        mock_response_post = Mock()
        mock_response_post.json.return_value = {"detail": "Internal Server Error"}
        mock_response_post.status_code = 500
        mock_post.return_value = mock_response_post

        user_data = add_user_data()

        mock_post.assert_called_with(
            "http://localhost:8000/users",
            json={
                "username": "piyush1",
                "email": "piyushkag11@gmail.com",
                "model_computed_fields": "some_computed_field",
                "posts": []
            }
        )
        self.assertEqual(mock_response_post.status_code, 500)
        self.assertEqual(user_data, {"detail": "Internal Server Error"})
        logger.success("Passed - Test Case to handle internal server error for add user.")

    @patch("requests.delete")
    def test_delete_user(self, mock_delete):
        mock_response = Mock()
        response_dict = {
            "detail": "User deleted"
        }
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_delete.return_value = mock_response

        delete_response = delete_user_by_id(1)

        mock_delete.assert_called_with("http://localhost:8000/users/1")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(delete_response, response_dict)
        logger.info("Passed - Test Case to delete user.")

    @patch("requests.delete")
    def test_delete_user_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "User not found."}
        mock_response.status_code = 404
        mock_delete.return_value = mock_response

        delete_response = delete_user_by_id(999)

        mock_delete.assert_called_with("http://localhost:8000/users/999")
        self.assertEqual(mock_response.status_code, 404)
        self.assertEqual(delete_response, {"detail": "User not found."})
        logger.info("Passed - Test Case to handle user not found for delete user.")

    @patch("requests.post")
    def test_fetch_users_from_tp_api(self, mock_post):
        mock_response = Mock()
        response_dict = {"message": "Users have been successfully fetched and stored."}
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = fetch_users_from_tp_api()

        mock_post.assert_called_with("http://localhost:8000/fetch-users-from-tp-api")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(response, response_dict)
        logger.info("Passed - Test Case to fetch users from third-party API.")

    @patch("requests.get")
    def test_get_all_users(self, mock_get):
        mock_response = Mock()
        response_dict = [
            {"username": "pk", "email": "pk@gmail.com", "id": 1},
            {"username": "piyush1", "email": "piyushkag11@gmail.com", "id": 14}
        ]
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        users_data = get_all_users()

        mock_get.assert_called_with("http://localhost:8000/users/")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(users_data, response_dict)
        logger.info("Passed - Test Case to get all users.")

    @patch("requests.get")
    def test_get_all_users_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "No users found."}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        users_data = get_all_users()

        mock_get.assert_called_with("http://localhost:8000/users/")
        self.assertEqual(mock_response.status_code, 404)
        self.assertEqual(users_data, {"detail": "No users found."})
        logger.info("Passed - Test Case to handle no users found for get all users.")

    @patch("requests.get")
    def test_get_user_by_word(self, mock_get):
        mock_response = Mock()
        response_dict = ["pk", "piyush1"]
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        users_data = get_user_by_word("pk")

        mock_get.assert_called_with("http://localhost:8000/byword/pk")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(users_data, response_dict)
        logger.info("Passed - Test Case to get user by word.")

    @patch("requests.get")
    def test_get_user_by_word_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "User not found."}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        users_data = get_user_by_word("nonexistent")

        mock_get.assert_called_with("http://localhost:8000/byword/nonexistent")
        self.assertEqual(mock_response.status_code, 404)
        self.assertEqual(users_data, {"detail": "User not found."})
        logger.info("Passed - Test Case to handle user not found for get user by word.")

    @patch("requests.get")
    def test_get_paginated_users(self, mock_get):
        mock_response = Mock()
        response_dict = [
            {"username": "pk", "email": "pk@gmail.com", "id": 1},
            {"username": "piyush1", "email": "piyushkag11@gmail.com", "id": 14}
        ]
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        users_data = get_paginated_users(5)

        mock_get.assert_called_with("http://localhost:8000/paginated-users/?limit=5")
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(users_data, response_dict)
        logger.info("Passed - Test Case to get paginated users.")

    @patch("requests.get")
    def test_get_paginated_users_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "No users found."}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        users_data = get_paginated_users(5)

        mock_get.assert_called_with("http://localhost:8000/paginated-users/?limit=5")
        self.assertEqual(mock_response.status_code, 404)
        self.assertEqual(users_data, {"detail": "No users found."})
        logger.info("Passed - Test Case to handle no users found for get paginated users.")


if __name__ == '__main__':
    unittest.main()
