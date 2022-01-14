#!/bin/bash
cd build
CC={{cookiecutter.cc}} CXX={{cookiecutter.cxx}} conan install .. --build=missing --profile={{cookiecutter.project_name}} -s compiler.libcxx=libstdc++11
cmake --configure ..
cd ..
