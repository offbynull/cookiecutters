# Hook: pre_gen_project
# Exec timing: After questions but before template process - allows validating variables and conditionally pulling in extra files/dirs
# Working dir: Root of the generated project
# Template variables: Yes

import re
import subprocess
import shutil

def try_int(s: str):
    try:
        return int(s)
    except ValueError:
        return s

def find_pip_package_version(
    package: str,
    version_pattern: str = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'  # semver
) -> tuple[int | str, ...]:
    print(f'Checking version of Python package {package}: ', end='')
    python_exe_path = shutil.which('python3') or shutil.which('python')
    p = subprocess.run([python_exe_path, '-m', 'pip', 'show', package], capture_output=True, text=True, check=True)
    m_list = re.findall(
        version_pattern,
        str(p.stdout)
    )
    if len(m_list) == 0:
        raise ValueError(f'No version found\n\n{m_list}\n\n{p.stdout}')
    print(m_list[0])
    return tuple(try_int(g) for g in m_list[0])

PROJECT_NAME_PATTERN = r'[0-9a-z_]+'

if __name__ == '__main__':
    if not re.fullmatch(PROJECT_NAME_PATTERN, {{ cookiecutter.project_name | pprint}}):
        raise ValueError({{ cookiecutter.project_name | pprint }} + f' does not conform to expected pattern {PROJECT_NAME_PATTERN}')
    {% if cookiecutter.include_python_extension != 'na' -%}
    python_build_ver = find_pip_package_version('build')
    if not(python_build_ver[0:2] >= (1, 0)):
        raise ValueError(f'Bad python build version {python_build_ver}')
    {%- endif %}
    ...