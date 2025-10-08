# Hook: post_gen_project
# Exec timing: After the project generation - allows cleaning up of extra files/dirs
# Working dir: Root of the generated project
# Template variables: Yes

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
    {% if cookiecutter.include_gtest %}
    run(['meson', 'wrap', 'install', 'gtest'])
    {% endif %}
    run(['meson', 'setup', '--reconfigure', 'buildDir', '--buildtype=debug'])
    run(['meson', 'compile', '-C', 'buildDir'])
    print('The project has been successfully created!')
    print()
    print('README.md contents:')
    with open('README.md', 'r') as f:
        content = f.read()
        print(content, end='')
