
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import your FastAPI app
import main 

import unittest
from unittest import mock
from fastapi import status
from fastapi.testclient import TestClient
from routers.GeneralRouters import GeneralRouter

app = main.app