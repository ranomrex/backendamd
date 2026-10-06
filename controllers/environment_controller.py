"""Sets up a Java or Python development environment (uses winget, so Windows)."""
import os
import subprocess
import sys

JAVA_TEMPLATE = """public class Main {
    public static void main(String[] args) {
        System.out.println("Java environment ready");
    }
}
"""


def _installed(command):
    """True if running the command works, e.g. ['java', '-version']."""
    try:
        return subprocess.run(command, capture_output=True, text=True).returncode == 0
    except FileNotFoundError:
        return False


def _winget_install(package_id):
    try:
        subprocess.run(["winget", "install", "-e", "--id", package_id], check=True)
        return True
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Install failed: {e}")
        return False


def setup_java_environment(project_name="MyJavaApp"):
    print("Setting up Java environment...")
    if _installed(["java", "-version"]):
        print("Java is already installed.")
    elif not _winget_install("Oracle.JDK.21"):
        return

    src_path = os.path.join(project_name, "src")
    os.makedirs(src_path, exist_ok=True)
    main_file = os.path.join(src_path, "Main.java")
    if not os.path.exists(main_file):
        with open(main_file, "w") as f:
            f.write(JAVA_TEMPLATE)
        print("Created Main.java.")
    print("Java environment ready.")


def setup_python_environment(project_name="myproject"):
    print("Setting up Python environment...")
    python = sys.executable  # the interpreter already running this script
    os.makedirs(project_name, exist_ok=True)

    venv_path = os.path.join(project_name, "venv")
    subprocess.run([python, "-m", "venv", venv_path], check=True)
    print("Virtual environment created.")

    bin_dir = "Scripts" if os.name == "nt" else "bin"
    pip = os.path.join(venv_path, bin_dir, "pip")
    subprocess.run([pip, "install", "requests", "psutil"], check=True)
    print("Python environment ready.")


def handle_environment_task(task_data):
    env_type = task_data.get("environment")
    if env_type == "java":
        setup_java_environment(task_data.get("project_name", "MyJavaApp"))
    elif env_type == "python":
        setup_python_environment(task_data.get("project_name", "myproject"))
    else:
        print(f"Unknown environment: {env_type}")
