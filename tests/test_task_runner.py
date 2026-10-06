from controllers import task_runner


def test_unknown_task_is_reported():
    result = task_runner.run_task({"task": "does_not_exist"})
    assert result["status"] == "error" and "unknown task" in result["error"]


def test_missing_fields_are_reported():
    result = task_runner.run_task({"task": "rename_files_in_folder"})
    assert result["status"] == "error"
    assert "target_folder" in result["error"] and "files_to_rename" in result["error"]


def test_accepts_action_key_as_well_as_task(monkeypatch):
    called = []
    monkeypatch.setitem(task_runner.HANDLERS, "undo", lambda data: called.append(data))
    result = task_runner.run_task({"action": "undo"})
    assert result["status"] == "ok" and called == [{"action": "undo"}]


def test_a_failing_handler_does_not_crash_the_runner(monkeypatch):
    def boom(data):
        raise RuntimeError("disk on fire")
    monkeypatch.setitem(task_runner.HANDLERS, "undo", boom)
    result = task_runner.run_task({"task": "undo"})
    assert result == {"task": "undo", "status": "error", "error": "disk on fire"}
