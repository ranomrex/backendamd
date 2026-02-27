import os
import json

HISTORY_FILE = "history.json"

def handle_file_task(task_data):
    task_name = task_data.get("task")

    # --- 1. RENAME LOGIC ---
    if task_name == "rename_files_in_folder":
        folder = task_data.get("target_folder", "")
        rename_map = task_data.get("files_to_rename", {})
        
        if folder and not os.path.exists(folder):
            print(f"Error: The folder '{folder}' does not exist.")
            return

        history_log = {
            "action_type": "rename_files",
            "folder": folder, 
            "renamed_files": {}
        }

        for old_name, new_name in rename_map.items():
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            
            if os.path.exists(old_path):
                try:
                    os.rename(old_path, new_path)
                    print(f"Success: Renamed '{old_name}' to '{new_name}'")
                    history_log["renamed_files"][old_name] = new_name
                except Exception as e:
                    print(f"Error renaming '{old_name}': {e}")
            else:
                print(f"Warning: '{old_path}' not found.")
        
        if history_log["renamed_files"]:
            with open(HISTORY_FILE, "w") as f:
                json.dump(history_log, f, indent=4)
            print("Action saved to history. You can now use the 'undo' task.")

    # --- 2. UNDO LOGIC ---
    elif task_name == "undo":
        if not os.path.exists(HISTORY_FILE):
            print("No history found. Nothing to undo.")
            return
        
        with open(HISTORY_FILE, "r") as f:
            history_log = json.load(f)
            
        if history_log.get("action_type") != "rename_files":
            print("Last action was not a file rename. Cannot undo.")
            return

        folder = history_log.get("folder", "")
        renamed_files = history_log.get("renamed_files", {})

        for original_name, current_name in renamed_files.items():
            current_path = os.path.join(folder, current_name)
            original_path = os.path.join(folder, original_name)
            
            if os.path.exists(current_path):
                try:
                    os.rename(current_path, original_path)
                    print(f"Success: Undid rename. '{current_name}' is back to '{original_name}'")
                except Exception as e:
                    print(f"Error undoing '{current_name}': {e}")
            else:
                print(f"Warning: '{current_path}' not found.")
        
        os.remove(HISTORY_FILE)
        print("Undo complete. History cleared.")
    
    else:
        print("Task action not recognized by File Manager.")