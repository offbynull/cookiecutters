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

def run(cmd: list[str]):
    print(f'Running {cmd}')
    p = subprocess.run(cmd, capture_output=True, check=False)
    if p.returncode != 0:
        print(p.stdout)
        print(p.stderr)
        raise ValueError('Failed')

if __name__ == '__main__':
    {% if cookiecutter.include_unittests %}
    run(['meson', 'wrap', 'install', 'gtest'])
    run(['meson', 'setup', '--reconfigure', 'buildDir'])
    {% endif %}
    ...
