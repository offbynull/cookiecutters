project('{{ cookiecutter.project_name }}', 'cpp',
        version : '1.0.0',
        default_options : ['warning_level=everything', 'cpp_std=c++23'])


dependencies = []

{% if cookiecutter.include_boost %}
# Include boost dependency
# ------------------------
boost_dep = dependency('boost', modules : ['container', 'filesystem', 'iostreams'])
dependencies += [boost_dep]
{% endif %}

{% if cookiecutter.include_source_checker %}
# Load source checker target
# --------------------------
python3 = find_program('python3', required: true)
source_checker = custom_target(
        'source_checker',
        command: ['python3', meson.current_source_dir() + '/source_checker.py'],
        output: ['unused'],
        build_always_stale: true
)
{% endif %}

{% if cookiecutter.include_doxygen %}
# Load doxygen target
# -------------------
python3 = find_program('python3', required: true)
dot = find_program('dot', required: true)
doxygen = find_program('doxygen', required: true)
doc_generator = custom_target(
        'doc_generator',
        command: ['python3', meson.current_source_dir() + '/source_doxygen_runner.py'],
        output : ['docs'],
        build_always_stale: true
)
{% endif %}

# Configure options
# -----------------
base_override_options = []
base_debug_override_options = base_override_options + ['optimization=0', 'buildtype=debug', 'b_lto=false', 'b_ndebug=false', 'debug=true', 'cpp_debugstl=true']
base_release_override_options = base_override_options +['optimization=3', 'buildtype=release', 'b_lto=true', 'b_ndebug=true', 'debug=false', 'cpp_debugstl=false']
cc = meson.get_compiler('cpp')
if cc.get_id() == 'gcc' or cc.get_id() == 'clang'
        # Configure base arguments for compiling / linking
        # ------------------------------------------------
        base_cpp_args = []
        base_link_args = []
        # Disable padding notification warning: Don't care about the compiler padding a struct.
        base_cpp_args += ['-Wno-padded']
        # Disable missing noexcept warning: Don't care that functions can be marked with noexcept.
        base_cpp_args += ['-Wno-noexcept']
        # Disable ignoring inline warning: When function implementations are placed inside of class definitions, it's a hint to the
        # compiler to inline the function. If it can't inline the function (or it doesn't inline it because it seems like a bad idea), it
        # puts out a -Winline warning. This only shows up when compiling at higher optimization levels.
        base_cpp_args += ['-Wno-inline']
        # Disable superfluous packing warning: When packing a struct, the compiler issues a warning if the struct is exactly the same
        # size in its packed form vs its padded form (because all members are already aligned). These warnings are being supressed because
        # the intention is for these structs to be packed, even if packing does nothing. In the future, should such a struct ever change
        # such that members are no longer aligned, the packing will ensure padding stays out.
        base_cpp_args += ['-Wno-packed']
        # Disable warnings specific to g++ extensions: These warnings are about applying extensions specific to g++. It doesn't apply to
        # portable C++ code. As such, don't care about them.
        base_cpp_args += ['-Wno-suggest-attribute=pure', '-Wno-suggest-attribute=const']
        # Unsure how to handle this, but it seems safe to ignore as this library requires a relatively new version of g++ and STL.
        base_cpp_args += ['-Wno-abi-tag']
        # Enable more robust compiler diagnostics
        base_cpp_args += ['-fconcepts-diagnostics-depth=9999', '-ftemplate-backtrace-limit=0']

        # Configure debug arguments for compiling / linking
        # ------------------------------------------------
        base_debug_cpp_args = base_cpp_args
        base_debug_link_args = base_link_args      
        # Enable standard library debugging.
        base_debug_cpp_args += ['-D_GLIBCXX_DEBUG']
        # Enable Google sanititzers.
        # DON'T USE THIS? MESON HAS b_sanitize OPTION?
        # san_args = ['-fsanitize=undefined', '-fsanitize=thread']
        # if cc.get_id() == 'clang'
        #         # Only available in clang -- doesn't really matter because I use valgrind for these.
        #         san_args += ['-fsanitize=memory']
        #         san_args += ['-fsanitize=leak']
        #         san_args += ['-fsanitize=address']
        # endif
        # debug_cpp_args += san_args
        # debug_link_args += san_args

        # Configure release arguments for compiling / linking
        # ---------------------------------------------------
        base_release_cpp_args = base_cpp_args
        base_release_link_args = base_link_args
else
        base_cpp_args = []
        base_link_args = []
        base_debug_cpp_args = base_cpp_args + []
        base_debug_link_args = base_link_args + []
        base_release_cpp_args = base_cpp_args + []
        base_release_link_args = base_link_args + []
endif

{% if cookiecutter.include_cli %}
# Create CLI executables
# ----------------------
cli_sources = [
        'cli.cpp'
]
cli_debug = executable(
        '{{ cookiecutter.project_name }}_cli_debug',
        cli_sources,
        {% if cookiecutter.include_source_checker %} source_checker {% endif %},
        {% if cookiecutter.include_doxygen %} doc_generator {% endif %},
        dependencies: dependencies,
        override_options: base_debug_override_options,
        cpp_args: base_debug_cpp_args,
        link_args: base_debug_link_args
)
cli_release = executable(
        '{{ cookiecutter.project_name }}_cli_release',
        cli_sources,
        {% if cookiecutter.include_source_checker %} source_checker {% endif %},
        {% if cookiecutter.include_doxygen %} doc_generator {% endif %},
        dependencies: dependencies,
        override_options: base_release_override_options,
        cpp_args: base_release_cpp_args,
        link_args: base_release_link_args
)
{% endif %}


{% if cookiecutter.include_unittests %}
# Create unittest executables
# ---------------------------
gtest = subproject('gtest')
gtest_dep = gtest.get_variable('gtest_dep')
gmock_dep = gtest.get_variable('gmock_dep')
gtest_sources = [
        'gtest-all.cpp',
        '{{ cookiecutter.project_name }}/math/helpers_test.cpp'
]
gtest_debug = executable(
        '{{ cookiecutter.project_name }}_gtest_debug',
        gtest_sources,
        dependencies: dependencies,
        override_options: base_debug_override_options,
        cpp_args: base_debug_cpp_args,
        link_args: base_debug_link_args
)
test('gtest_debug', gtest_debug)
gtest_release = executable(
        '{{ cookiecutter.project_name }}_gtest_release',
        gtest_sources,
        dependencies: dependencies,
        override_options: base_release_override_options,
        cpp_args: base_release_cpp_args,
        link_args: base_release_link_args
)
test('gtest_release', gtest_release)
{% endif %}


{% if cookiecutter.include_python_extension != 'false' %}
# Create python extension
# -----------------------
py = import('python')
py_installation = py.find_installation(
        pure: false,
        modules: [{% if cookiecutter.include_python_extension == 'true_with_numpy' %}'numpy'{% endif %}]
)
{% if cookiecutter.include_python_extension == 'true_with_numpy' %}
py_numpy_include_dir = run_command(
        py_installation.full_path(),
        ['-c', 'import numpy; print(numpy.get_include())'],
        check: true
).stdout().strip()
py_includes = include_directories(py_numpy_include_dir)
{% else %}
py_includes = include_directories()
{% endif %}
py_sources = [
        '{{ cookiecutter.project_name }}/python/python_extension.h'
]
py_debug = py_installation.extension_module(
        '{{ cookiecutter.project_name }}_python_debug',
        py_sources,
        {% if cookiecutter.include_source_checker %} source_checker {% endif %},
        {% if cookiecutter.include_doxygen %} doc_generator {% endif %},
        install: true,
        dependencies: dependencies,
        include_directories: py_includes,
        override_options: base_debug_override_options,
        cpp_args: base_debug_cpp_args,
        link_args: base_debug_link_args
)
py_release = py_installation.extension_module(
        '{{ cookiecutter.project_name }}_python_release',
        py_sources,
        {% if cookiecutter.include_source_checker %} source_checker {% endif %},
        {% if cookiecutter.include_doxygen %} doc_generator {% endif %},
        install: true,
        dependencies: dependencies,
        include_directories: py_includes,
        override_options: base_release_override_options,
        cpp_args: base_release_cpp_args,
        link_args: base_release_link_args
)
{% endif %}
