"""FastAPI service that exposes the task runner over HTTP.
Run with: uvicorn src.main:app --reload   (docs at /docs)
"""
from typing import Any, Dict, List, Union

from fastapi import FastAPI, HTTPException

from controllers import task_runner

app = FastAPI(title="backendamd", description="Run local automation tasks over HTTP")


@app.get("/")
def home():
    return {"message": "backendamd is running"}


@app.get("/tasks")
def list_tasks():
    """Lists the task names the runner understands and the fields each needs."""
    return task_runner.REQUIRED_FIELDS


@app.post("/run")
def run(tasks: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Runs one task or a list of tasks and returns a result for each."""
    batch = tasks if isinstance(tasks, list) else [tasks]
    for task in batch:
        error = task_runner.validate(task)
        if error:
            raise HTTPException(status_code=422, detail=error)
    return [task_runner.run_task(task) for task in batch]
