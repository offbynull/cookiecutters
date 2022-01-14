#!/bin/bash
cd build
conan install .. --build=missing --profile={{cookiecutter.project_name}} -s compiler.libcxx=libstdc++20
cmake --configure ..
cd ..
