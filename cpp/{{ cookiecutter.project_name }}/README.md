# {{ cookiecutter.project_name }}

To configure buildtype:

* `meson configure buildDir -Dbuildtype=debug`
* `meson configure buildDir -Dbuildtype=release`
* `meson configure buildDir -Dbuildtype=debugoptimized`
* `meson configure buildDir -Dbuildtype=minsize`
* `meson configure buildDir -Dbuildtype=plain`

{% if cookiecutter.include_cli -%}
To compile and run command-line interface:

* `meson compile -C buildDir cli`
* `./buildDir/cli`
{%- endif %}

{% if cookiecutter.include_gtest -%}
To compile and run GUnit unittests:

* `meson compile -C buildDir gtest`
* `./buildDir/gtest`
{%- endif %}

{% if cookiecutter.include_python_extension != 'false' -%}
To compile and run Python extension:

* `cd {{ cookiecutter.project_name }}`
* `pip install .`
* `cd ..` (exit dir running the next command, otherwise python will look in current dir for {{ cookiecutter.project_name }})
* `python3 -c "import  {{ cookiecutter.project_name }}.math.helpers as h; print(h.average([1,2,3,4,5]))"`
* `pip uninstall {{ cookiecutter.project_name }}`

To build Python wheel:

* `pip install build`
* `python3 -m build --wheel` (builds wheel for the OS/arch that's running the command)
{%- endif %}