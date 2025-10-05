# Python interface stubs used to assist type checkers. Required because these are native functions, and so type
# checkers can't automatically suss out the type like they can with regular non-native python functions.

from typing import Iterable

def sum_of_squares(nums: Iterable[int]) -> int: ...
def average(nums: Iterable[int]) -> float: ...
