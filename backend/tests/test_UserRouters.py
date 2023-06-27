import unittest
from fastapi.testclient import TestClient

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main
from authentication.authentication import pwd_context, users_collections


UserRouter = main.UserRouter
# Create a test client for the FastAPI app
client = TestClient(UserRouter)

# Dummy unit test file
# class UserAuthenticationTests(unittest.TestCase):
#     def setUp(self):
#         self.valid_user_registration = {
#             "firstname": "John",
#             "lastname": "Doe",
#             "username": "johndoe",
#             "email": "johndoe@example.com",
#             "password": "password",
#             "phonenumber": "1234567890",
#             "profilepicture": "profile.jpg"
#         }
#         self.valid_user_login = {
#             "username": "johndoe",
#             "password": "password"
#         }

#     def tearDown(self):
#         # Clean up any test data or state
#         users_collections.delete_many({})

#     def test_register_existing_username(self):
#         # Insert a user with the same username as the one being registered
#         users_collections.insert_one({"username": "johndoe"})
#         response = client.post("/user/auth/register", json=self.valid_user_registration)
#         self.assertEqual(response.status_code, 409)
#         self.assertEqual(response.json(), {"detail": "Username already exists"})

#     def test_register_success(self):
#         response = client.post("/user/auth/register", json=self.valid_user_registration)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json().get("message"), "User Registered Successfully")

#     def test_login_nonexistent_username(self):
#         response = client.post("/user/auth/login", json=self.valid_user_login)
#         self.assertEqual(response.status_code, 409)
#         self.assertEqual(response.json(), {"detail": "Username already exists"})

#     def test_login_invalid_password(self):
#         # Insert a user with the same username and a different password
#         users_collections.insert_one({"username": "johndoe", "password": "incorrect_password"})
#         response = client.post("/user/auth/login", json=self.valid_user_login)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json(), {"detail": "Invalid user name or password"})

#     def test_login_already_logged_in(self):
#         # Insert a user with the same username and isloggedin set to True
#         users_collections.insert_one({"username": "johndoe", "isloggedin": True})
#         response = client.post("/user/auth/login", json=self.valid_user_login)
#         self.assertEqual(response.status_code, 409)
#         self.assertEqual(response.json(), {"detail": "User is already logged in"})

#     def test_login_success(self):
#         # Insert a user with the same username and password
#         users_collections.insert_one({"username": "johndoe", "password": pwd_context.hash("password")})
#         response = client.post("/user/auth/login", json=self.valid_user_login)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json().get("message"), "User Login Successfully")

#     def test_logout(self):
#         # Insert a user with the same username and set isloggedin to True
#         users_collections.insert_one({"username": "johndoe", "isloggedin": True})
#         response = client.post("/user/auth/logout", headers={"Authorization": "Bearer token"})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"Message": "Logout Successfully"})


if __name__ == "__main__":
    unittest.main()
