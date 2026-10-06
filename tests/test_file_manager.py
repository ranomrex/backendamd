import json

from controllers import file_manager


def test_rename_then_undo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # history.json is written to the current folder
    (tmp_path / "a.txt").write_text("hello")

    file_manager.handle_file_task({
        "task": "rename_files_in_folder",
        "target_folder": str(tmp_path),
        "files_to_rename": {"a.txt": "b.txt"},
    })
    assert (tmp_path / "b.txt").exists() and not (tmp_path / "a.txt").exists()
    assert json.loads((tmp_path / "history.json").read_text())["renamed_files"] == {"a.txt": "b.txt"}

    file_manager.handle_file_task({"task": "undo"})
    assert (tmp_path / "a.txt").exists() and not (tmp_path / "b.txt").exists()
    assert not (tmp_path / "history.json").exists()


def test_does_not_overwrite_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "a.txt").write_text("one")
    (tmp_path / "b.txt").write_text("two")

    file_manager.rename_files(str(tmp_path), {"a.txt": "b.txt"})
    assert (tmp_path / "a.txt").read_text() == "one"
    assert (tmp_path / "b.txt").read_text() == "two"


def test_undo_with_no_history(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    file_manager.undo_last_rename()
    assert "Nothing to undo" in capsys.readouterr().out
