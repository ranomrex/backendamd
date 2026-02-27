from controllers import environment_controller
from controllers import file_manager  
from controllers import window_manager 

def run_task(task_data):
    task_name = task_data.get("task") or task_data.get("action")

    # Route Environments
    if task_name == "setup_environment":
        print("Routing to Environment Controller...")
        environment_controller.handle_environment_task(task_data)

    # Route File Operations (Rename AND Undo)
    elif task_name in ["rename_files_in_folder", "undo"]:
        print("Routing to File Manager...")
        file_manager.handle_file_task(task_data) 

    # Route Window Splits
    elif task_name == "open_split_screen":
        print("Routing to Window Manager...")
        window_manager.handle_window_task(task_data)

    else:
        print(f"Unknown task: {task_name}")