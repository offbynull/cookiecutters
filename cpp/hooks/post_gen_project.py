# Hook: post_gen_project
# Exec timing: After the project generation - allows cleaning up of extra files/dirs
# Working dir: Root of the generated project
# Template variables: Yes

import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

def run(cmd: list[str]):
    print(f'Running {cmd}: ', end='')
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', prefix='postgen_', suffix='.log', delete=False) as tf:
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
        # Check for invalid configs.
        {% if 'boost' in cookiecutter.include_python_extension and cookiecutter.boost_version == 'na' -%}
        raise ValueError('Unable to use boost for python extension because you have chosen not to install boost')
        {%- endif %}
        # Install wraps.
        {% if cookiecutter.include_gtest -%}
        run(['meson', 'wrap', 'install', 'gtest'])
        {%- endif %}
        {% if 'pybind11' in cookiecutter.include_python_extension -%}
        run(['meson', 'wrap', 'install', 'pybind11'])
        {%- endif %}
        # Setup project (download wraps as well).
        run(['meson', 'setup', '--reconfigure', 'buildDir', '--buildtype=release'])
        {% if cookiecutter.include_gtest -%}
        # Remove meson.build from .gitignore files within wraps: Some wraps have .gitignores that ends up ignoring the meson.build for that
        # wrap. When you commit, CI builds fail if meson.build isn't present.
        print('Removing meson.build from .gitignore in downloaded wraps')
        for p in Path('subprojects').rglob('.gitignore'):
            print(f'> {p}')
            s = p.read_text(encoding='utf-8')
            p.write_text(s + '\n!meson.build\n', encoding='utf-8')
        # Sanity checks.
        run(['meson', 'test', '-C', 'buildDir', '-v', 'gtest'])
        {%- endif %}
        {% if cookiecutter.include_cli -%}
        run(['meson', 'compile', '-C', 'buildDir', 'cli'])
        {%- endif %}
        {% if cookiecutter.include_python_extension != 'na' -%}
        python_exe_path = shutil.which('python3') or shutil.which('python')
        run([python_exe_path, '-m', 'build', '--wheel'])  # Existance of 'build' module should have been confirmed in pre_gen_project.py
        print('WARNING: Do not build wheels with buildtype=debug.')
        {%- endif %}
    except Exception as e:
        raise ValueError('Execution failed - Is meson failing with SSL verification errors? Try "pip install pip-system-certs"') from e