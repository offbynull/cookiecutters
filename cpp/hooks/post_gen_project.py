# Hook: post_gen_project
# Exec timing: After the project generation - allows cleaning up of extra files/dirs
# Working dir: Root of the generated project
# Template variables: Yes

# EXAMPLE
# -------
# import os
#
# REMOVE_PATHS = [
#     '{% if 'pip' in cookiecutter.project_name %}requirements.txt{% endif %}',
#     '{% if 'poetry' in cookiecutter.project_name %}poetry.lock{% endif %}',
# ]
#
# for path in REMOVE_PATHS:
#     path = path.strip()
#     if path and os.path.exists(path):
#         os.unlink(path) if os.path.isfile(path) else os.rmdir(path)
import sys
import subprocess

def is_docker_installed() -> bool:
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        return True
    except Exception:
        return False

if __name__ == '__main__':
    {% if cookiecutter.include_unittests %}
    try:
        subprocess.run(['meson', 'wrap', 'install', 'gtest'], capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print("Exit Code:", e.returncode)
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
    except FileNotFoundError:
        print("Error: Command not found.")
    {% endif %}
    ...
