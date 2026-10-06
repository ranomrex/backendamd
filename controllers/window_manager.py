"""Opens apps and arranges their windows on screen (needs a display)."""
import subprocess
import time


def handle_window_task(task_data):
    # Imported here so the rest of the project works on a machine with no display.
    import pyautogui
    import pygetwindow as gw

    apps = task_data.get("apps", {})  # {window title keyword: command to launch}
    screen_width, screen_height = pyautogui.size()

    windows = []
    for title, command in apps.items():
        print(f"Opening {command}...")
        subprocess.Popen(command, shell=True)
        time.sleep(2)  # give the app time to appear
        found = gw.getWindowsWithTitle(title)
        if found:
            windows.append(found[0])
        else:
            print(f"Warning: no window with '{title}' in its title.")

    if len(windows) == 1:
        windows[0].maximize()
        print("Maximized the window.")
    elif len(windows) == 2:
        left, right = windows
        left.restore()
        right.restore()
        left.moveTo(0, 0)
        left.resizeTo(screen_width // 2, screen_height)
        right.moveTo(screen_width // 2, 0)
        right.resizeTo(screen_width // 2, screen_height)
        print("Arranged the windows side by side.")
    elif len(windows) > 2:
        print("Split screen supports 2 windows. The apps are open but not arranged.")
