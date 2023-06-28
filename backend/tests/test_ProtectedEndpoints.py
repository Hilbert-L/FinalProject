import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your FastAPI app