"""Dispatcher: validates a task, sends it to the controller that handles it,
and returns a result dict so callers (the CLI and the API) can report status."""
from controllers import environment_controller, file_manager, window_manager

# task name -> function that handles it
HANDLERS = {
    "setup_environment": environment_controller.handle_environment_task,
    "rename_files_in_folder": file_manager.handle_file_task,
    "undo": file_manager.handle_file_task,
    "open_split_screen": window_manager.handle_window_task,
}

# task name -> fields it must have
REQUIRED_FIELDS = {
    "setup_environment": ["environment", "project_name"],
    "rename_files_in_folder": ["target_folder", "files_to_rename"],
    "undo": [],
    "open_split_screen": ["apps"],
}


def validate(task_data):
    """Returns an error message, or None if the task looks fine."""
    if not isinstance(task_data, dict):
        return "task must be a JSON object"
    name = task_data.get("task") or task_data.get("action")
    if name not in HANDLERS:
        return f"unknown task: {name}"
    missing = [f for f in REQUIRED_FIELDS[name] if f not in task_data]
    if missing:
        return f"missing field(s): {', '.join(missing)}"
    return None


def run_task(task_data):
    """Runs one task. Returns {"task": name, "status": "ok" | "error", "error": msg}."""
    error = validate(task_data)
    name = task_data.get("task") or task_data.get("action") if isinstance(task_data, dict) else None
    if error:
        print(f"Skipped '{name}': {error}")
        return {"task": name, "status": "error", "error": error}

    handler = HANDLERS[name]
    print(f"Running '{name}' with {handler.__module__}...")
    try:
        handler(task_data)
    except Exception as e:  # one bad task should not stop the rest
        print(f"Task '{name}' failed: {e}")
        return {"task": name, "status": "error", "error": str(e)}
    return {"task": name, "status": "ok", "error": None}
