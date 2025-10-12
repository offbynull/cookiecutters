# cpp cookiecutter

Cookiecutter template for a modern C++ project. Each project rendered using this template ...

* uses meson as its build system.
* uses GitHub actions to test and build across multiple targets.
* can optionally include a simple scaffolding for a CLI (via main function).
* can optionally include infrastructure for unittesting (via GUnit).
* can optionally include infrastructure for Python C extensions.

The template does its best to support a wide range of configurations: Operating systems, platforms, and architectures. However, some options may not work on certain configurations (e.g., at the time of writing, meson identifies msvc as not supporting the c++23 standard).