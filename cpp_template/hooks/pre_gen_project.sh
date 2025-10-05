#!/bin/bash
if [ ! -x "$(which {{cookiecutter.cc}})" ] ; then
    echo "CC MISSING: Unable to find {{cookiecutter.cc}}"
    exit 1
fi
if [ ! -x "$(which {{cookiecutter.cxx}})" ] ; then
    echo "CXX MISSING: Unable to find {{cookiecutter.cxx}}"
    exit 1
fi
if [ ! -x "$(which cmake)" ] ; then
    echo "CMAKE MISSING: Unable to find cmake"
    exit 1
fi
if [ ! -x "$(which conan)" ] ; then
    echo "CONAN MISSING: Unable to find conan"
    exit 1
fi