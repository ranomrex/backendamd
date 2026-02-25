from controllers.environment_controller import (
    setup_java_environment,
    setup_python_environment
)


def run_task(task_data):

    if task_data["task"] == "setup_environment":

        if task_data["environment"] == "java":
            project_name = task_data.get("project_name", "MyJavaApp")
            setup_java_environment(project_name)

        elif task_data["environment"] == "python":
            project_name = task_data.get("project_name", "myproject")
            setup_python_environment(project_name)

        else:
            print("Unknown environment.")

    else:
        print("Unknown task.")