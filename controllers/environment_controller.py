import subprocess
import sys
import os

def setup_java_environment(project_name="MyJavaApp"):
    print("Setting up Java Development Environment...")
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Java is already installed.")
        else:
            raise Exception
    except Exception:
        print("Java not found. Installing...")
        try:
            subprocess.run(["winget", "install", "-e", "--id", "Oracle.JDK.21"], check=True)
            print("Java installed successfully.")
        except Exception as e:
            print("Java installation failed:", e)
            return

    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"Created project folder: {project_name}")

    src_path = os.path.join(project_name, "src")
    if not os.path.exists(src_path):
        os.makedirs(src_path)

    main_file_path = os.path.join(src_path, "Main.java")
    if not os.path.exists(main_file_path):
        with open(main_file_path, "w") as file:
            file.write("""public class Main {
    public static void main(String[] args) {
        System.out.println("Java environment ready 🚀");
    }
}
""")
        print("Created Main.java template.")
    print("Java environment setup completed successfully.")


def setup_python_environment(project_name="myproject"):
    print("Setting up Python Development Environment...")
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Python found:", result.stdout.strip())
        else:
            raise Exception
    except Exception:
        print("Python not found. Installing...")
        try:
            subprocess.run(["winget", "install", "-e", "--id", "Python.Python.3"], check=True)
            print("Python installed successfully.")
        except Exception as e:
            print("Python installation failed:", e)
            return

    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"])

    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"Created project folder: {project_name}")

    venv_path = os.path.join(project_name, "venv")
    subprocess.run(["python", "-m", "venv", venv_path], check=True)
    print("Virtual environment created.")

    pip_path = os.path.join(venv_path, "Scripts", "pip")
    subprocess.run([pip_path, "install", "requests"])
    subprocess.run([pip_path, "install", "psutil"])

    print("Basic packages installed.")
    print("Python environment setup completed successfully.")

# --- THE DISPATCHER LISTENER ---
def handle_environment_task(task_data):
    env_type = task_data.get("environment")
    if env_type == "java":
        project_name = task_data.get("project_name", "MyJavaApp")
        setup_java_environment(project_name)
    elif env_type == "python":
        project_name = task_data.get("project_name", "myproject")
        setup_python_environment(project_name)
    else:
        print("Unknown environment.")