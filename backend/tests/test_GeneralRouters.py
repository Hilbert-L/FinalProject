import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Import your FastAPI app
from main import app

import unittest
from unittest import mock
from fastapi import status
from routers.GeneralRouters import GeneralRouter

class GeneralRouterTestCase(unittest.TestCase):

    @mock.patch("app.users_collections")
    def test_get_users(self, mock_users_collections):
        # Mock the return value of users_collections.find()
        mock_users = [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"}
        ]
        
        mock_users_collections.find.return_value = mock_users

        # Perform the request
        response = GeneralRouter.get("/users")

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"users": mock_users})

    @mock.patch("app.admin_collections")
    def test_get_admins(self, mock_admin_collections):
        # Mock the return value of admin_collections.find()
        mock_admins = [
            {"username": "admin1", "email": "admin1@example.com"},
            {"username": "admin2", "email": "admin2@example.com"}
        ]
        mock_admin_collections.find.return_value = mock_admins

        # Perform the request
        response = GeneralRouter.get("/admins")

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"admins": mock_admins})

    @mock.patch("app.car_space_collections")
    def test_get_car_spaces(self, mock_car_space_collections):
        # Mock the return value of car_space_collections.find()
        mock_car_spaces = [
            {"name": "Space1", "location": "Location1"},
            {"name": "Space2", "location": "Location2"}
        ]
        mock_car_space_collections.find.return_value = mock_car_spaces

        # Perform the request
        response = GeneralRouter.get("/carspace")

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"car_spaces": mock_car_spaces})

    @mock.patch("app.car_space_review_collections")
    def test_get_car_space_reviews(self, mock_car_space_review_collections):
        # Mock the return value of car_space_review_collections.find()
        mock_car_space_reviews = [
            {"rating": 5, "comment": "Great space"},
            {"rating": 4, "comment": "Nice location"}
        ]
        mock_car_space_review_collections.find.return_value = mock_car_space_reviews

        # Perform the request
        response = GeneralRouter.get("/carspacereviews")

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"carspace_reviews": mock_car_space_reviews})


if __name__ == "__main__":
    unittest.main()