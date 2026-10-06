from controllers import task_runner


def test_unknown_task_is_reported(capsys):
    task_runner.run_task({"task": "does_not_exist"})
    assert "Unknown task" in capsys.readouterr().out


def test_accepts_action_key_as_well_as_task(monkeypatch):
    called = []
    monkeypatch.setitem(task_runner.HANDLERS, "undo", lambda data: called.append(data))
    task_runner.run_task({"action": "undo"})
    assert called == [{"action": "undo"}]
