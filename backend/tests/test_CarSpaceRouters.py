import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# # Import your FastAPI app
from main import app

import os

# Get the path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)

# Get the root directory by going up multiple levels
root_directory = os.path.dirname(current_directory)
