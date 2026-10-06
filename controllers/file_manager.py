"""Batch file rename with a saved history, so the last rename can be undone."""
import json
import os

HISTORY_FILE = "history.json"


def handle_file_task(task_data):
    name = task_data.get("task")
    if name == "rename_files_in_folder":
        rename_files(task_data.get("target_folder", ""), task_data.get("files_to_rename", {}))
    elif name == "undo":
        undo_last_rename()
    else:
        print("Task not recognized by File Manager.")


def rename_files(folder, rename_map):
    """Renames {old_name: new_name} inside folder and saves what changed."""
    if folder and not os.path.exists(folder):
        print(f"Error: the folder '{folder}' does not exist.")
        return

    renamed = {}
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(folder, old_name)
        new_path = os.path.join(folder, new_name)
        if not os.path.exists(old_path):
            print(f"Warning: '{old_path}' not found.")
            continue
        if os.path.exists(new_path):
            print(f"Skipped: '{new_name}' already exists.")
            continue
        try:
            os.rename(old_path, new_path)
        except OSError as e:
            print(f"Error renaming '{old_name}': {e}")
            continue
        print(f"Renamed '{old_name}' to '{new_name}'")
        renamed[old_name] = new_name

    if renamed:
        with open(HISTORY_FILE, "w") as f:
            json.dump({"action_type": "rename_files", "folder": folder, "renamed_files": renamed}, f, indent=4)
        print("Saved to history. Use the 'undo' task to reverse it.")


def undo_last_rename():
    """Reverses the rename saved in the history file, then clears the history."""
    if not os.path.exists(HISTORY_FILE):
        print("No history found. Nothing to undo.")
        return

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    if history.get("action_type") != "rename_files":
        print("Last action was not a file rename. Cannot undo.")
        return

    folder = history.get("folder", "")
    for original_name, current_name in history.get("renamed_files", {}).items():
        current_path = os.path.join(folder, current_name)
        original_path = os.path.join(folder, original_name)
        if not os.path.exists(current_path):
            print(f"Warning: '{current_path}' not found.")
            continue
        try:
            os.rename(current_path, original_path)
            print(f"Undid rename: '{current_name}' is back to '{original_name}'")
        except OSError as e:
            print(f"Error undoing '{current_name}': {e}")

    os.remove(HISTORY_FILE)
    print("Undo complete. History cleared.")
