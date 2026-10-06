"""Dispatcher: sends each task to the controller that handles it."""
from controllers import environment_controller, file_manager, window_manager

# task name -> function that handles it
HANDLERS = {
    "setup_environment": environment_controller.handle_environment_task,
    "rename_files_in_folder": file_manager.handle_file_task,
    "undo": file_manager.handle_file_task,
    "open_split_screen": window_manager.handle_window_task,
}


def run_task(task_data):
    name = task_data.get("task") or task_data.get("action")
    handler = HANDLERS.get(name)
    if handler is None:
        print(f"Unknown task: {name}")
        return
    print(f"Running '{name}' with {handler.__module__}...")
    handler(task_data)
