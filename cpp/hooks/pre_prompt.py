# Hook: pre_prompt
# Exec timing: Before any question is rendered.
# Working dir: Copy of the repository directory, allowing rewrite of cookiecutter.json.
# Template variables: No

import re
import subprocess

def try_int(s: str):
    try:
        return int(s)
    except ValueError:
        return s

def invoke_and_extract_version(
    cmd: list[str],
    version_pattern: str = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'  # semver
) -> tuple[int | str, ...]:
    print(f'Checking version {cmd}: ', end='')
    p = subprocess.run(cmd, capture_output=True, check=True)
    m_list = re.findall(
        version_pattern,
        str(p.stdout)
    )
    if len(m_list) == 0:
        raise ValueError(f'No version found\n\n{m_list}\n\n{p.stdout}')
    print(m_list[0])
    return tuple(try_int(g) for g in m_list[0])

if __name__ == '__main__':
    gcc_ver = invoke_and_extract_version(['g++', '--version'])
    if not(gcc_ver[0:2] >= (14, 2)):
        raise ValueError(f'Bad g++ version {gcc_ver}')
    python_ver = invoke_and_extract_version(['python3', '--version'])
    if not(python_ver[0:2] >= (3, 12)):
        raise ValueError(f'Bad python version {python_ver}')
    meson_ver = invoke_and_extract_version(['meson', '--version'])
    if not(meson_ver[0:3] >= (1, 5, 1)):
        raise ValueError(f'Bad meson version {meson_ver}')