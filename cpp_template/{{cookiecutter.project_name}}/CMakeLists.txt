cmake_minimum_required(VERSION 3.14)

# set the project name
project(MyProject)

include(build/conanbuildinfo.cmake)
conan_basic_setup()

# add the executable
file(GLOB_RECURSE main_sources CONFIGURE_DEPENDS src/main/*.cpp)
add_executable(main ${main_sources})

file(GLOB_RECURSE test_sources CONFIGURE_DEPENDS src/test/*.cpp)
add_executable(test ${test_sources})

target_link_libraries(main ${CONAN_LIBS})
target_link_libraries(test ${CONAN_LIBS})

target_compile_features(main PRIVATE cxx_std_20)
target_compile_features(test PRIVATE cxx_std_20)
target_compile_options(main PRIVATE -Werror -Wall -Wextra -Wconversion -Wsign-conversion -pedantic-errors)
target_compile_options(test PRIVATE -Werror -Wall -Wextra -Wconversion -Wsign-conversion -pedantic-errors)
# https://www.foonathan.net/2018/10/cmake-warnings/
target_compile_options(main PRIVATE
    $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:GNU>>:-Werror -Wall -Wextra -Wconversion -Wsign-conversion -pedantic-errors>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
)
target_compile_options(test PRIVATE
    $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:GNU>>:-Werror -Wall -Wextra -Wconversion -Wsign-conversion -pedantic-errors>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
)
