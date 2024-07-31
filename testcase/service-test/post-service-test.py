import unittest
from unittest.mock import Mock, patch

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from service import post_service
from schemas import PostBase
from loguru import logger
from fastapi import HTTPException


class TestPostService(unittest.TestCase):

    def setUp(self):
        self.db = Mock(spec=Session)

    @patch('repository.post_repo.create_post')
    def test_create_post(self, mock_create_post):
        post_data = PostBase(id=1, title="Test Post", content="Content here", user_id=1)

        post_service.create_post(self.db, post_data)
        created_post = mock_create_post.call_args[0][1]
        mock_create_post.assert_called_once_with(self.db, created_post)
        logger.success("Test case Passed for creating post.")

        mock_create_post.side_effect = Exception("Database error")
        with self.assertRaises(HTTPException) as context:
            post_service.create_post(self.db, post_data)
        self.assertEqual(context.exception.detail, "Database error")
        self.assertEqual(context.exception.status_code, 500)
        logger.success("Test case Passed for handling exception in creating post.")

    @patch('repository.post_repo.get_post')
    def test_get_post(self, mock_get_post):
        mock_get_post.return_value = {"id": 1, "title": "Test Post", "content": "Content here", "user_id": 1}
        result = post_service.get_post(self.db, 1)
        self.assertEqual(result, {"id": 1, "title": "Test Post", "content": "Content here", "user_id": 1})
        logger.success("Test case Passed for getting post.")

        mock_get_post.side_effect = Exception("Database error")
        with self.assertRaises(HTTPException) as context:
            post_service.get_post(self.db, 1)
        self.assertEqual(context.exception.detail, "Database error")
        self.assertEqual(context.exception.status_code, 500)
        logger.success("Test case Passed for handling exception in getting post.")

    @patch('repository.post_repo.get_posts')
    def test_get_posts(self, mock_get_posts):
        mock_get_posts.return_value = [{"id": 1, "title": "Test Post", "content": "Content here", "user_id": 1}]
        result = post_service.get_posts(self.db)
        self.assertEqual(result, [{"id": 1, "title": "Test Post", "content": "Content here", "user_id": 1}])
        logger.success("Test case Passed for getting posts.")

        mock_get_posts.side_effect = Exception("Database error")
        with self.assertRaises(HTTPException) as context:
            post_service.get_posts(self.db)
        self.assertEqual(context.exception.detail, "Database error")
        self.assertEqual(context.exception.status_code, 500)
        logger.success("Test case Passed for handling exception in getting posts.")

    @patch('repository.post_repo.delete_post')
    def test_delete_post(self, mock_delete_post):
        post_service.delete_post(self.db, 1)
        mock_delete_post.assert_called_once_with(self.db, 1)
        logger.success("Test case Passed for deleting post.")

        mock_delete_post.side_effect = Exception("Database error")
        with self.assertRaises(HTTPException) as context:
            post_service.delete_post(self.db, 1)
        self.assertEqual(context.exception.detail, "Database error")
        self.assertEqual(context.exception.status_code, 500)
        logger.success("Test case Passed for handling exception in deleting post.")

    @patch('repository.post_repo.get_post')
    def test_get_post_by_word(self, mock_get_post):
        # Mock database session
        self.db = mock_get_post.return_value

        # Test case for successfully getting a post by word
        self.db.query().filter().all.return_value = [
            ("Test Post",)
        ]
        result = post_service.get_post_by_word(self.db, 'Test')
        self.assertEqual(result, ["Test Post"])
        logger.success("Test case Passed for getting post by word")

        # Test case for no post found with the given word
        self.db.query().filter().all.return_value = []
        with self.assertRaises(HTTPException) as context:
            post_service.get_post_by_word(self.db, "None")
        self.assertEqual(context.exception.detail, "Post not found with word None")
        self.assertEqual(context.exception.status_code, 404)
        logger.success("Test case Passed for handling exception in getting post by word.")

        # Test case for handling unexpected exceptions
        self.db.query().filter().all.side_effect = SQLAlchemyError("Database error")
        with self.assertRaises(HTTPException) as context:
            post_service.get_post_by_word(self.db, 'Test')
        self.assertEqual(context.exception.detail, "Database error")
        self.assertEqual(context.exception.status_code, 500)
        logger.success("Test case Passed for handling unexpected exception in getting post by word.")


if __name__ == "__main__":
    unittest.main()
