import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from services.auth import get_current_user

client = TestClient(app)

def override_auth():
    return {"username": "testuser"}

app.dependency_overrides[get_current_user] = override_auth

def test_list_vms_return_200():
    mock_nodes = [{"node": "homelab"}]
    mock_vms = [
        {"vmid": 100, "name": "test-vm", "status": "running"},
        {"vmid": 101, "name": "test-vm-2", "status": "stopped"},
    ]

    with patch("endpoints.virtual_machines.prox") as mock_prox:
        mock_prox.nodes.get.return_value = mock_nodes
        mock_prox.nodes.return_value.qemu.get.return_value = mock_vms
        response = client.get("/v1/vms")
        assert response.status_code == 200
        assert len(response.json()) == 2

def test_get_vm_200():
    mock_vm = {"vmid": 100, "name": "test-vm", "status": "running"}

    with patch("endpoints.virtual_machines.prox") as mock_prox:
        mock_prox.nodes.return_value.qemu.return_value.status.current.get.return_value = mock_vm
        response = client.get("/v1/vms/100")
        assert response.status_code == 200
        assert response.json()["vmid"] == 100
        assert response.json()["name"] == "test-vm"

def test_start_vm():
    mock_upid = "UPID:homelab:0034029F:0C0433D8:6A6AC092:qmstart:100:glambert@pam!proxmoxer:"

    with patch("endpoints.virtual_machines.prox") as mock_prox, \
        patch("endpoints.virtual_machines.log_action") as mock_log:
        mock_prox.nodes.return_value.qemu.return_value.status.start.post.return_value = mock_upid
        response = client.post("/v1/vms/100/start")
        assert response.status_code == 200
        assert "UPID" in response.json()

def test_stop_vm():
    mock_upid = "UPID:homelab:0034029F:0C0433D8:6A6AC092:qmstart:100:glambert@pam!proxmoxer:"

    with patch("endpoints.virtual_machines.prox") as mock_prox, \
        patch("endpoints.virtual_machines.log_action") as mock_log:
        mock_prox.nodes.return_value.qemu.return_value.status.stop.post.return_value = mock_upid
        response = client.post("/v1/vms/100/stop")
        assert response.status_code == 200
        assert "UPID" in response.json()
