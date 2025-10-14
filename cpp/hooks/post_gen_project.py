# Hook: post_gen_project
# Exec timing: After the project generation - allows cleaning up of extra files/dirs
# Working dir: Root of the generated project
# Template variables: Yes

import sys
import subprocess

def run(cmd: list[str]):
    print(f'Running {cmd}')
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if p.returncode != 0:
        print(p.stdout)
        print(p.stderr)
        raise ValueError('Failed')

if __name__ == '__main__':
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
        run(['python', '-m', 'build', '--wheel'])
        print('WARNING: Wheel built as a release buildtype regardless of what buildtype is set to.')
        {%- endif %}
    except Exception as e:
        raise ValueError('Execution failed - Is meson failing with SSL verification errors? Try "pip install pip-system-certs"') from e
    print('The project has been successfully created!')
    print()
    print('README.md contents:')
    with open('README.md', 'r') as f:
        content = f.read()
        print(content, end='')
