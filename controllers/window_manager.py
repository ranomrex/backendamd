import os
import json
import subprocess
import time
import pyautogui
import pygetwindow as gw

HISTORY_FILE = "history.json"

def run_task(task_data):
    action = task_data.get("action")

       # REnaming files



def run_task(task_data):
    if task_data.get("action") == "rename_files_in_folder":
        folder = task_data.get("target_folder", "")
        rename_map = task_data.get("files_to_rename", {})
        
        # Check if the specified folder actually exists
        if folder and not os.path.exists(folder):
            print(f"Error: The folder '{folder}' does not exist.")
            return

        for old_name, new_name in rename_map.items():
            # Combine the folder path with the filenames
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            
            if os.path.exists(old_path):
                try:
                    os.rename(old_path, new_path)
                    print(f"Success: Renamed '{old_name}' to '{new_name}' in '{folder}'")
                except Exception as e:
                    print(f"Error renaming '{old_name}': {e}")
            else:
                print(f"Warning: The file '{old_path}' does not exist.")
    else:
        print("Task action not recognized.")


        # Undo function

        import os
import json

# Define where to save our memory
HISTORY_FILE = "history.json"

def run_task(task_data):
    action = task_data.get("action")

    # --- 1. RENAME LOGIC (Now with memory) ---
    if action == "rename_files_in_folder":
        folder = task_data.get("target_folder", "")
        rename_map = task_data.get("files_to_rename", {})
        
        if folder and not os.path.exists(folder):
            print(f"Error: The folder '{folder}' does not exist.")
            return

        # Create a dictionary to remember what actually got renamed
        history_log = {"folder": folder, "renamed_files": {}}

        for old_name, new_name in rename_map.items():
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            
            if os.path.exists(old_path):
                try:
                    os.rename(old_path, new_path)
                    print(f"Success: Renamed '{old_name}' to '{new_name}'")
                    # Log it for the undo function
                    history_log["renamed_files"][old_name] = new_name
                except Exception as e:
                    print(f"Error renaming '{old_name}': {e}")
            else:
                print(f"Warning: '{old_path}' not found.")
        
        # Save the memory to a file
        if history_log["renamed_files"]:
            with open(HISTORY_FILE, "w") as f:
                json.dump(history_log, f, indent=4)
            print("Action saved to history. You can now undo this.")

    # --- 2. TRUE UNDO LOGIC ---
    elif action == "undo":
        # Check if we have a memory file
        if not os.path.exists(HISTORY_FILE):
            print("No history found. Nothing to undo.")
            return
        
        # Read the memory
        with open(HISTORY_FILE, "r") as f:
            history_log = json.load(f)
        
        folder = history_log.get("folder", "")
        renamed_files = history_log.get("renamed_files", {})

        # Reverse the actions
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
        
        # Delete the memory file so we don't accidentally undo twice
        os.remove(HISTORY_FILE)
        print("Undo complete. History cleared.")
        
    else:
        print("Task action not recognized.")


    # --- NEW SPLIT SCREEN LOGIC ---
        import subprocess
import time
import pyautogui
import pygetwindow as gw

def handle_window_task(task_data):
    # We already know the action is "open_split_screen" because task_runner routed it here!
    # So we just grab the apps list directly from the JSON.
    apps_to_open = task_data.get("apps", {})
    opened_windows = []
    
    # Get your monitor's resolution
    screen_width, screen_height = pyautogui.size()
    
    # Step 1: Open the apps and find their windows
    for window_title, command in apps_to_open.items():
        print(f"Opening {command}...")
        
        # Launch the application
        subprocess.Popen(command, shell=True)
        
        # Wait 2 seconds for the app to actually load on screen
        time.sleep(2) 
        
        # Search for the window using the title keyword
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            opened_windows.append(windows[0])
            print(f"Grabbed window for '{window_title}'")
        else:
            print(f"Warning: Opened '{command}' but couldn't find a window containing '{window_title}' in the title bar.")
    
    # Step 2: Arrange the windows
    num_apps = len(opened_windows)
    
    if num_apps == 1:
        # If only one app, just maximize it
        opened_windows[0].maximize()
        print("Maximized the single window.")
        
    elif num_apps == 2:
        # If two apps, split them side-by-side
        win1, win2 = opened_windows[0], opened_windows[1]
        
        # Un-maximize them first so they can be resized
        win1.restore()
        win2.restore()
        
        # Move App 1 to top-left (0,0) and make it half the width
        win1.moveTo(0, 0)
        win1.resizeTo(screen_width // 2, screen_height)
        
        # Move App 2 to the top-middle and make it half the width
        win2.moveTo(screen_width // 2, 0)
        win2.resizeTo(screen_width // 2, screen_height)
        
        print("Successfully arranged windows in a 50/50 split screen!")
        
    elif num_apps > 2:
        print("Apps are open, but split-screen is currently only configured for 2 windows.")