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
