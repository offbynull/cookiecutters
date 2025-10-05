import {{ cookiecutter.project_name }}._native.{{ cookiecutter.project_name }}_python_extension as _native_extension

def sum_of_squares(nums: list[int]) -> int:
    return _native_extension.sum_of_squares(nums)

def average(nums: list[int]) -> float:
    return _native_extension.average(nums)
