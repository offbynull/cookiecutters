# Hook: pre_prompt
# Exec timing: Before any question is rendered.
# Working dir: Copy of the repository directory, allowing rewrite of cookiecutter.json.
# Template variables: No

import re
import subprocess
import sys
import os
import shutil
from pathlib import Path
from enum import Enum

def try_int(s: str):
    try:
        return int(s)
    except ValueError:
        return s

class CaptureFrom(Enum):
    STDOUT = 0
    STDERR = 1
    STDOUT_AND_STDERR = 2

def invoke_and_extract_version(
    cmd: list[str],
    capture_from:  CaptureFrom = CaptureFrom.STDOUT,
    version_pattern: str = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'  # semver
) -> tuple[int | str, ...]:
    print(f'Checking version {cmd}: ', end='')
    p = subprocess.run(cmd, capture_output=True, text=True, check=True)
    if capture_from == CaptureFrom.STDOUT:
        p_out = p.stdout
    elif capture_from == CaptureFrom.STDERR:
        p_out = p.stderr
    elif capture_from == CaptureFrom.STDOUT_AND_STDERR:
        p_out = p.stdout + p.stderr
    else:
        raise ValueError('This should never happen')
    m_list = re.findall(
        version_pattern,
        str(p_out)
    )
    if len(m_list) == 0:
        raise ValueError(f'No version found\n\n{m_list}\n\n{p_out}')
    print(m_list[0])
    return tuple(try_int(g) for g in m_list[0])

MIN_EXPECTED_GCC_VER = (14, 2)

MIN_EXPECTED_CLANG_VER = (20, 0)

MIN_EXPECTED_MSVC_VER = (19, 43)

if __name__ == '__main__':
    # Compiler test
    compiler_path = os.getenv('CXX')
    if compiler_path is not None:
        compiler_path = Path(compiler_path)
        if compiler_path.name in {'g++', 'g++.exe'}:
            gcc_ver = invoke_and_extract_version(['g++', '--version'])
            print(f'  {gcc_ver} should be >= {MIN_EXPECTED_GCC_VER} for good c++20 support')
        elif compiler_path.name in {'clang++', 'clang++.exe'}:
            clang_ver = invoke_and_extract_version(['clang++', '--version'])
            print(f'  {clang_ver=} should be >= {MIN_EXPECTED_CLANG_VER} for good c++20 support')
        elif compiler_path.name in {'cl.exe'}:
            msvc_ver = invoke_and_extract_version(['cl.exe'], CaptureFrom.STDOUT_AND_STDERR)
            print(f'  {msvc_ver=} should be >= {MIN_EXPECTED_MSVC_VER} for good c++20 support')
        else:
            print(f'WARNING: CXX on path but compiler not recognized: {msvc_ver}', file=sys.stderr)
    else:
        found_compiler = False
        if shutil.which('g++'):
            gcc_ver = invoke_and_extract_version(['g++', '--version'])
            print(f'  {gcc_ver} should be >= {MIN_EXPECTED_GCC_VER} for good c++20 support')
            found_compiler = True
        if shutil.which('clang++'):
            clang_ver = invoke_and_extract_version(['clang++', '--version'])
            print(f'  {clang_ver=} should be >= {MIN_EXPECTED_CLANG_VER} for good c++20 support')
            found_compiler = True
        if shutil.which('cl.exe'):
            msvc_ver = invoke_and_extract_version(['cl.exe'], CaptureFrom.STDOUT_AND_STDERR)
            print(f'  {msvc_ver=} should be >= {MIN_EXPECTED_MSVC_VER} for good c++20 support')
            found_compiler = True
        if not found_compiler:
            raise ValueError('WARNING: No compiler found - meson may not configure the project properly')
    # Py test
    python_exe_path = shutil.which('python3') or shutil.which('python')
    if python_exe_path is None:
        raise ValueError('Python not found')
    python_ver = invoke_and_extract_version([python_exe_path, '--version'])
    if not(python_ver[0:2] >= (3, 12)):
        raise ValueError(f'Bad python version {python_ver}')
    # Meson test
    meson_exe_path = shutil.which('meson')
    if meson_exe_path is None:
        raise ValueError('Meson not found')
    meson_ver = invoke_and_extract_version([meson_exe_path, '--version'])
    if not(meson_ver[0:3] >= (1, 5, 1)):
        raise ValueError(f'Bad meson version {meson_ver}')