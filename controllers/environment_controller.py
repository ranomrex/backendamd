import subprocess
import sys
import os

#java environment setup function
def setup_java_environment(project_name="MyJavaApp"):
    print("Setting up Java Development Environment...")

    # Step 1: Check if Java is installed
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Java is already installed.")
        else:
            raise Exception

    except Exception:
        print("Java not found. Installing...")

        try:
            subprocess.run(
                ["winget", "install", "-e", "--id", "Oracle.JDK.21"],
                check=True
            )
            print("Java installed successfully.")
        except Exception as e:
            print("Java installation failed:", e)
            return

    # Step 2: Create Project Folder
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"Created project folder: {project_name}")

    # Step 3: Create src folder
    src_path = os.path.join(project_name, "src")
    if not os.path.exists(src_path):
        os.makedirs(src_path)

    # Step 4: Create Main.java template
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





#Python environment setup function
def setup_python_environment(project_name="myproject"):
    print("Setting up Python Development Environment...")

    # Step 1: Check if Python is installed
    try:
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Python found:", result.stdout.strip())
        else:
            raise Exception

    except Exception:
        print("Python not found. Installing...")

        # Install Python using winget (Windows)
        try:
            subprocess.run(
                ["winget", "install", "-e", "--id", "Python.Python.3"],
                check=True
            )
            print("Python installed successfully.")
        except Exception as e:
            print("Python installation failed:", e)
            return

    # Step 2: Upgrade pip
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"])

    # Step 3: Create Project Folder
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"Created project folder: {project_name}")

    # Step 4: Create Virtual Environment
    venv_path = os.path.join(project_name, "venv")

    subprocess.run(
        ["python", "-m", "venv", venv_path],
        check=True
    )

    print("Virtual environment created.")

    # Step 5: Install common dev tools inside venv
    pip_path = os.path.join(venv_path, "Scripts", "pip")

    subprocess.run([pip_path, "install", "requests"])
    subprocess.run([pip_path, "install", "psutil"])

    print("Basic packages installed.")
    print("Python environment setup completed successfully.")