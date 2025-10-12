# Hook: pre_gen_project
# Exec timing: After questions but before template process - allows validating variables and conditionally pulling in extra files/dirs
# Working dir: Root of the generated project
# Template variables: Yes

# EXAMPLE
# -------
# import re
# import sys
#
# MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
# project_name = '{{ cookiecutter.project_name }}'
#
# if not re.match(MODULE_REGEX, project_name):
#     print(f'ERROR: {project_name} is not a valid Python module name!')
#     sys.exit(1)