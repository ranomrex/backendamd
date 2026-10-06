"""Entry point: reads a JSON task file and runs each task.

Usage:
    python run.py                    # reads tasks.json
    python run.py my_tasks.json      # reads another file
Exit code is 1 if any task failed.
"""
import json
import sys

from controllers.task_runner import run_task


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "tasks.json"
    try:
        with open(path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise SystemExit(f"Task file '{path}' not found.")
    except json.JSONDecodeError as e:
        raise SystemExit(f"'{path}' is not valid JSON: {e}")

    # A file can hold one task (an object) or several (a list).
    tasks = data if isinstance(data, list) else [data]
    results = [run_task(task) for task in tasks]

    failed = [r for r in results if r["status"] == "error"]
    print(f"\nDone: {len(results) - len(failed)} ok, {len(failed)} failed.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
