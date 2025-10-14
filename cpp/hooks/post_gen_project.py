# Hook: post_gen_project
# Exec timing: After the project generation - allows cleaning up of extra files/dirs
# Working dir: Root of the generated project
# Template variables: Yes

import sys
import subprocess
import shutil
import tempfile

def run(cmd: list[str]):
    print(f'Running {cmd}: ', end='')
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", prefix="postgen_", suffix=".log", delete=False) as tf:
        tf.write(f'exit={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}')
        fname = tf.name
    if p.returncode == 0:
        print(f'Passed ({fname})')
    else:
        print(f'**FAILED** ({fname})')

if __name__ == '__main__':
    print('The project has been successfully created!')
    print()
    print('README.md contents:')
    with open('README.md', 'r') as f:
        content = f.read()
        print(content)
    print()
    try:
        {% if cookiecutter.include_gtest -%}
        run(['meson', 'wrap', 'install', 'gtest'])
        {%- endif %}
        run(['meson', 'setup', '--reconfigure', 'buildDir', '--buildtype=debug'])
        {% if cookiecutter.include_gtest -%}
        run(['meson', 'test', '-C', 'buildDir', '-v', 'gtest'])
        {%- endif %}
        {% if cookiecutter.include_cli -%}
        run(['meson', 'compile', '-C', 'buildDir', 'cli'])
        {%- endif %}
        {% if cookiecutter.include_python_extension != 'na' -%}
        python_exe_path = shutil.which('python3') or shutil.which('python')
        run([python_exe_path, '-m', 'build', '--wheel'])  # Existance of "build" module should have been confirmed in pre_gen_project.py
        print('WARNING: Wheel built as a release buildtype regardless of what meson\'s buildtype was set to.')
        {%- endif %}
    except Exception as e:
        raise ValueError('Execution failed - Is meson failing with SSL verification errors? Try "pip install pip-system-certs"') from e