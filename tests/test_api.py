from fastapi.testclient import TestClient

from controllers import task_runner
from src.main import app

client = TestClient(app)


def test_home():
    assert client.get("/").status_code == 200


def test_list_tasks():
    assert set(client.get("/tasks").json()) == set(task_runner.HANDLERS)


def test_run_single_task(monkeypatch):
    monkeypatch.setitem(task_runner.HANDLERS, "undo", lambda data: None)
    r = client.post("/run", json={"task": "undo"})
    assert r.status_code == 200
    assert r.json() == [{"task": "undo", "status": "ok", "error": None}]


def test_run_rejects_bad_task():
    r = client.post("/run", json={"task": "nope"})
    assert r.status_code == 422
