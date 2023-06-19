import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Import your FastAPI app
from main import app