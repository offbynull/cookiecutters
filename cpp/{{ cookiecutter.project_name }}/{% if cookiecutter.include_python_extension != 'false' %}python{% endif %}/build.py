import os
import platform
from pathlib import Path
import shutil
import subprocess

def copy_single_using_glob(glob_pattern: str, src: Path, dst_dir: Path) -> None:
    p = next(iter(src.glob(glob_pattern)))
    shutil.copy2(p, dst_dir)
    dst_file = dst_dir / p.name
    return dst_file

def rename_stem_prefix(path: Path, old_prefix: str, new_prefix: str) -> Path:
    old_suffixes = '.'.join(path.suffixes)
    if not path.stem.startswith(old_prefix):
        raise ValueError('Bad prefix')
    new_stem = new_prefix + path.stem[len(old_prefix):]
    new_path = path.with_name(new_stem + old_suffixes)
    return path.rename(new_path)

cpp_dir = ...
python_dir = Path(__file__).parent

system = platform.system()
arch = platform.machine()
libc, _ = platform.libc_ver()

target_without_buildtype = '{{ cookiecutter.project_name }}_python_extension'
target = f'{target_without_buildtype}_release'

print('Compiling...')
subprocess.run(['meson', 'clean'], cwd=cpp_dir, capture_output=True, check=True)
subprocess.run(['meson', 'compile', target], cwd=cpp_dir, capture_output=True, check=True)

print('Copying...')
src_dir = cpp_dir
dst_dir = python_dir / '{{ cookiecutter.project_name }}' / '_native'
shutil.rmtree(dst_dir, ignore_errors=True)  # Remove existing directory (recursive delete)
dst_dir.mkdir(parents=True, exist_ok=False)
if system == 'Linux' and arch == 'x86_64' and libc == 'musl':
    dst_file = copy_single_using_glob(f'{target}*.so', src_dir, dst_dir)
elif system == 'Linux' and arch == 'x86_64':
    dst_file = copy_single_using_glob(f'{target}*.so', src_dir, dst_dir)
elif system == 'Linux' and arch in ('aarch64', 'arm64'):
    dst_file = copy_single_using_glob(f'{target}*.so', src_dir, dst_dir)
# elif system == 'Darwin' and arch == 'x86_64':
#     dst_file = copy_single_using_glob(f'{target}*.so', src_dir, dst_dir)
elif system == 'Darwin' and arch in ('aarch64', 'arm64'):
    dst_file = copy_single_using_glob(f'{target}*.so', src_dir, dst_dir)
elif system == 'Windows' and arch == 'AMD64':
    dst_file = copy_single_using_glob(f'{target}*.pyd', src_dir, dst_dir)
elif system == 'Windows' and arch == 'ARM64':
    dst_file = copy_single_using_glob(f'{target}*.pyd', src_dir, dst_dir)
else:
    raise RuntimeError(f'Unsupported platform: {system} {arch}')
rename_stem_prefix(path=dst_file, old_prefix=target, new_prefix=target_without_buildtype)