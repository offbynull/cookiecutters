#!/bin/bash
mkdir -p build
cd build
CC={{cookiecutter.cc}} CXX={{cookiecutter.cxx}} conan profile new {{cookiecutter.project_name}} --detect
# libcxx=libstdc++11 required because gtest is breaking: 
CC={{cookiecutter.cc}} CXX={{cookiecutter.cxx}} conan profile update settings.compiler.libcxx=libstdc++11 {{cookiecutter.project_name}}
CC={{cookiecutter.cc}} CXX={{cookiecutter.cxx}} conan install .. --build=missing --profile={{cookiecutter.project_name}}
CC={{cookiecutter.cc}} CXX={{cookiecutter.cxx}} cmake --configure ..
echo GO INTO {{cookiecutter.project_name}} PROJECT FOLDER AND TYPE cmake --build build TO MAKE A BUILD
echo GO INTO {{cookiecutter.project_name}} PROJECT FOLDER AND TYPE cmake --build build TO MAKE A BUILD
echo GO INTO {{cookiecutter.project_name}} PROJECT FOLDER AND TYPE cmake --build build TO MAKE A BUILD
echo GO INTO {{cookiecutter.project_name}} PROJECT FOLDER AND TYPE cmake --build build TO MAKE A BUILD
echo GO INTO {{cookiecutter.project_name}} PROJECT FOLDER AND TYPE cmake --build build TO MAKE A BUILD
cd ..
