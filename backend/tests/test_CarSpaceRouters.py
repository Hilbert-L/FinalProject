# Import your FastAPI app
import unittest
from unittest import mock

from fastapi import status
from routers.CarSpaceRouters import CarSpaceRouters


class CarSpaceRouterTestCase(unittest.TestCase):

    @mock.patch("app.car_space_collections")
    def test_get_car_spaces(self, mock_car_space_collections):
        # Mock the return value of car_space_collections.find()
        mock_car_spaces = [
            {"UserName": "username1", "Title": "Title1","Address":"Address1","Suburb":"Suburb1","Postcode":"Postcode1"},
            {"UserName": "username2", "Title": "Title2","Address":"Address2","Suburb":"Suburb2","Postcode":"Postcode2"}
        ]
        mock_car_space_collections.find.return_value = mock_car_spaces

        # Perform the request
        response = CarSpaceRouters.get("/car_spaces")

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"car_spaces": mock_car_spaces})

    @mock.patch("app.car_space_collections")
    def test_get_single_car_space(self, mock_car_space_collections):
        # Mock the return value of car_space_collections.find_one()
        mock_car_space = {"name": "Space1", "location": "Location1"}
        mock_car_space_collections.find_one.return_value = mock_car_space

        # Perform the request
        response = CarSpaceRouters.get("/car_spaces/Space1")

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"car_space": mock_car_space})

if __name__ == "__main__":
    unittest.main()