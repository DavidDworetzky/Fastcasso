from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi.testclient import TestClient
#import mocks for testing
from unittest.mock import patch

from ..main import app

client = TestClient(app)


def test_read_version():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().keys() == {"Version"}

