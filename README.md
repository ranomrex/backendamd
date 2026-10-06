# backendamd

A small Python backend that runs tasks on my laptop from a JSON file. I wrote it to stop repeating the same setup and file chores by hand: set up a Java or Python project, rename a pile of files, put two windows side by side.

## How it works

`run.py` reads a task (or a list of tasks) from JSON and hands each one to `controllers/task_runner.py`. The runner looks up the task name in a dictionary and calls the matching controller. Adding a new task means writing one handler and adding one line to that dictionary.

| Task | Controller | What it does |
|---|---|---|
| `setup_environment` | `environment_controller.py` | Creates a Java project (JDK 21 via winget, `Main.java` template) or a Python project (venv, installs `requests` and `psutil`) |
| `rename_files_in_folder` | `file_manager.py` | Renames files from a map you give it. Never overwrites an existing file. Saves what it did to `history.json` |
| `undo` | `file_manager.py` | Reverses the last rename using `history.json` |
| `open_split_screen` | `window_manager.py` | Opens two windows side by side with pyautogui and pygetwindow |

## Run it

```
pip install -r requirements.txt
cp tasks.example.json tasks.json
python run.py            # reads tasks.json
python run.py my_tasks.json
```

`tasks.example.json` has one example of each task. Edit it to point at your own folders.

## Tests

```
python -m pytest
```

Covers rename then undo, not overwriting an existing file, undo with no history, and unknown task names.

## API stub

`src/main.py` is a FastAPI app with two routes (`/` and `/item/{item_id}`). It is only a starting point for exposing the runner over HTTP, nothing is wired in yet.

```
uvicorn src.main:app --reload
```

## Limits

- The Java setup uses winget, so it is Windows only.
- The split screen task needs a real display. I have not covered it with tests.
- Tasks run one after another, with no retries.
