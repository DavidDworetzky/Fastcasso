from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi.testclient import TestClient
from PIL import Image
#import mocks for testing
from unittest import mock

from ..main import app

client = TestClient(app)

#Create Mock all white PNG
def mock_generate_image_diffusion():
    img = Image.new("RGB", (800, 1280), (255, 255, 255))
    return img

def test_read_version():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().keys() == {"Version"}

@mock.patch("app.mediators.image_diffusion.generate_image_diffusion")
def test_generate_image_endpoint(
    mock_generate_image_diffusion,
):
    mock_generate_image_diffusion.return_value = mock_generate_image_diffusion()
    response = client.get("/image/generate/this%20is%20a%20test/test.png")
    assert response.status_code == 200

