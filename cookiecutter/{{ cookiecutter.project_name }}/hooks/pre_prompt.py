# Hook: pre_prompt
# Exec timing: Before any question is rendered.
# Working dir: Copy of the repository directory, allowing rewrite of cookiecutter.json.
# Template variables: No

# EXAMPLE
# -------
# import sys
# import subprocess
#
# def is_docker_installed() -> bool:
#     try:
#         subprocess.run(["docker", "--version"], capture_output=True, check=True)
#         return True
#     except Exception:
#         return False
#
# if __name__ == "__main__":
#     if not is_docker_installed():
#         print("ERROR: Docker is not installed.")
#         sys.exit(1)
