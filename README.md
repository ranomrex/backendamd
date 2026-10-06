# backendamd

I got tired of doing the same small chores on my laptop again and again: setting up a new Java or Python project, renaming a pile of files, arranging two windows side by side. So I wrote a small Python backend that does them from a JSON file. I can also run it over HTTP.

## How I built it

Every task is a JSON object with a `"task"` name. I wrote a dispatcher in `controllers/task_runner.py` that checks the task is valid, then looks up the right controller in a dictionary and calls it. I did it this way so adding a new task only needs one new handler and one new line in the dictionary.

I also made sure one bad task does not kill the whole run. If a task fails, I catch the error, report it, and carry on with the next one.

These are the tasks I have so far:

| Task | Fields it needs | What it does |
|---|---|---|
| `setup_environment` | `environment`, `project_name` | Sets up a Java project (installs JDK 21 with winget and adds a `Main.java`) or a Python project (venv plus `requests` and `psutil`) |
| `rename_files_in_folder` | `target_folder`, `files_to_rename` | Renames files from an old name to new name map. It never overwrites a file that already exists, and it saves what it did to `history.json` |
| `undo` | none | Reverses the last rename using `history.json` |
| `open_split_screen` | `apps` | Opens two apps side by side using pyautogui and pygetwindow |

## Running it from the command line

```
pip install -r requirements.txt
python run.py              # reads tasks.json
python run.py other.json   # reads a different file
```

`tasks.json` can have one task or a list of them. This is what mine looks like:

```json
[
  {"task": "rename_files_in_folder", "target_folder": "demo", "files_to_rename": {"old.txt": "new.txt"}},
  {"task": "undo"}
]
```

At the end it prints how many tasks worked and how many failed. It exits with code 1 if anything failed, so I can use it in scripts.

## Running it as an API

I added a FastAPI layer so I can send tasks over HTTP instead of editing a file.

```
uvicorn src.main:app --reload
```

- `GET /tasks` lists the tasks and the fields each one needs.
- `POST /run` runs one task or a list of tasks and gives back a status for each. If a task is invalid it returns a 422.

FastAPI also gives me interactive docs at `http://127.0.0.1:8000/docs`.

## Tests

```
python -m pytest
```

I wrote 11 tests. They cover rename and undo, not overwriting files, undo when there is no history, task validation, a failing handler not stopping the runner, and the API routes.

## What it can't do yet

- The Java setup uses winget, so it only works on Windows.
- I have not written tests for the split screen task because it needs a real display.
- Tasks run one after another, and there are no retries.
- The API runs real commands on the machine it is on, so I only run it locally and would not put it on the internet as it is.
