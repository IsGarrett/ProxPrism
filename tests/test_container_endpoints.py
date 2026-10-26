import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from services.auth import get_current_user

client = TestClient(app)

def override_auth():
    return {"username": "testuser"}


app.dependency_overrides[get_current_user] = override_auth


def test_list_all_containers():
    mock_lxc = [
        {"vmid": 100, "name": "test-lxc", "status": "running", "cpu": 0.1, "mem": 512},
        {"vmid": 101, "name": "test-lxc-2", "status": "stopped", "cpu": 0.0, "mem": 256},
    ]

    with patch("endpoints.containers.prox") as mock_prox:
        mock_prox.nodes.return_value.lxc.get.return_value = mock_lxc
        response = client.get("/v1/containers")
        assert response.status_code == 200
        assert len(response.json()) == 2

def test_get_container():
    mock_lxc = {"vmid": 100, "name": "test-lxc", "status": "running", "cpu": 0.1, "mem": 512}

    with patch("endpoints.containers.prox") as mock_prox:
        mock_prox.nodes.return_value.lxc.return_value.status.current.get.return_value = mock_lxc
        response = client.get("/v1/containers/100")
        assert response.status_code == 200
        assert response.json()['vmid'] == 100



        


