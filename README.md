# backendamd

A small Python backend that runs tasks on my laptop from a JSON file or over HTTP. I wrote it to stop repeating the same chores by hand: setting up a Java or Python project, renaming a pile of files, putting two windows side by side.

## How it works

Every task is a JSON object with a `"task"` name. `controllers/task_runner.py` checks that the task name is known and its required fields are present, then looks up the matching controller in a dictionary and calls it. If a task fails, the error is caught and reported, and the remaining tasks still run. Adding a new task means writing one handler and adding it to two dictionaries.

| Task | Needs | What it does |
|---|---|---|
| `setup_environment` | `environment`, `project_name` | Creates a Java project (JDK 21 via winget, `Main.java` template) or a Python project (venv, installs `requests` and `psutil`) |
| `rename_files_in_folder` | `target_folder`, `files_to_rename` | Renames files from an old-name to new-name map. Never overwrites an existing file. Saves what it did to `history.json` |
| `undo` | nothing | Reverses the last rename using `history.json` |
| `open_split_screen` | `apps` | Opens two apps side by side with pyautogui and pygetwindow |

## Run it from the command line

```
pip install -r requirements.txt
python run.py              # reads tasks.json
python run.py other.json   # reads another file
```

`tasks.json` can hold one task or a list:

```json
[
  {"task": "rename_files_in_folder", "target_folder": "demo", "files_to_rename": {"old.txt": "new.txt"}},
  {"task": "undo"}
]
```

It prints a summary at the end and exits with code 1 if any task failed.

## Run it as an API

```
uvicorn src.main:app --reload
```

| Route | What it does |
|---|---|
| `GET /tasks` | Lists the task names and the fields each one needs |
| `POST /run` | Runs one task or a list of tasks, returns a status for each. Returns 422 if a task is invalid |

Interactive docs are at `http://127.0.0.1:8000/docs`.

## Tests

```
python -m pytest
```

11 tests cover rename then undo, not overwriting files, undo with no history, validation, a failing handler not stopping the runner, and the API routes.

## Limits

- The Java setup uses winget, so it is Windows only.
- The split screen task needs a real display and is not covered by tests.
- Tasks run one after another, with no retries.
- The API runs real tasks on the machine it is on, so I only run it locally and do not expose it to the internet.
