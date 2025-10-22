from pathlib import Path

p = Path(__file__)
for file_path in path.iterdir():
    if file_path.is_file():
        if file_path.suffix in {'.h', '.hpp', '.c', '.cpp'}:
            raise ImportError('Running from source tree: Running from the source tree directory prevents wheels from loading because '
                              'Python packages within the directory that Python runs from (the source tree in this case) take precedence '
                              'over Python packages within site-packages. For example, if the directory you launched Python from contains '
                              'the package a.b and your Python instance's site-packages also contains the package a.b, importing a.b will '
                              'pick the one from the launch directory. In this case, this is a problem because the package from the '
                              'launch directory contains the Python C extension(s)'s source code, but not the compiled wheels that Python '
                              'needs to load. Leave the current directory and re-run Python.')