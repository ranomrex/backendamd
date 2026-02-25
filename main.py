import json
from src.task_runner import run_task

def main():
    with open("tasks.json", "r") as file:
        task_data = json.load(file)

    run_task(task_data)

if __name__ == "__main__":
    main()