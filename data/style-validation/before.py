# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Test cases for Isort and Yapf. '''


from __future__ import annotations

import types
import collections.abc as cabc
from typing import Any, Optional
from dataclasses import dataclass, field

import typing_extensions as typx
from other_third_party.submodule import (AnotherClass, OneMoreClass,
    VeryLongClassName,)
from some_third_party import ThirdPartyClass
from some_third_party.submodule import (AnotherClass, OneMoreClass,
    VeryLongClassName)

import emcd_testpkg as pkg
from emcd_testpkg.submodule import LocalClass


# Bracket alignment and dedenting

def test_bracket_alignment(first_arg, second_arg={
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}):
    values = [
        first_arg,
        second_arg['key1'],
        second_arg['key2']
    ]
    return values


# Function argument splitting variations

def simple_function(a, b, c=1, d=2): pass

def medium_function(first_positional, second_positional, first_named="some default", second_named="another default"): pass

def complex_function(really_long_positional_arg, another_long_positional_arg, yet_another_long_positional,
    first_named_arg="some very long default value", second_named_arg="another long default",
    third_named_arg="yet another default value that makes this very long"): pass

def very_complex_function(extremely_long_positional_argument_that_definitely_needs_its_own_line,
    another_extremely_long_positional_argument_that_needs_its_own_line,
    first_named_argument_that_is_very_long="some extremely long default value that won't fit",
    second_named_argument_that_is_very_long="another extremely long default value",
    third_named_argument_that_is_very_long="yet another extremely long default value"): pass

class TestClass:

    def method_with_many_args(self, first_arg, second_arg, first_kwarg="default", second_kwarg="default"): pass

    @classmethod
    def class_method_with_args(cls, first_arg, second_arg, first_kwarg="default", second_kwarg="default"): pass


# Dictionary formatting

meta = { 'key': 'value' }

meta_multiline = {
    'key1': 'value1',
    'key2': { 'nested': 'value' }
}

config = {
    'first_key': 'first_value',
    'second_key': {
        'nested_key1': 'nested_value1',
        'nested_key2': 'nested_value2'
    },
    'third_key': [
        'list_item1',
        'list_item2',
        'list_item3'
    ]
}


# List comprehensions and generator expressions

squares = [x * x for x in range(20) if x % 2 == 0]

complex_comp = [
    transform(x, y) for x in very_long_iterator_name
    for y in another_long_iterator
    if some_long_condition(x) and another_condition(y)
]

really_long_comprehension = [transform_function(x, y, z) for x in very_long_iterator_name for y in another_long_iterator_name for z in yet_another_iterator if some_complex_condition(x) and another_complex_condition(y) and final_condition(z)]


# Lambda expressions

simple_lambda = lambda x: x * 2

complex_lambda = lambda x, y, z: (
    some_long_computation(x) +
    another_computation(y) +
    final_computation(z))


# Function calls with mixed args

result = some_function(
    positional_arg1, positional_arg2,
    keyword_arg1="value1", keyword_arg2="value2")

result = very_long_function_name(
    first_positional_argument, second_positional_argument,
    first_keyword="first_value", second_keyword="second_value",
    third_keyword="third_value")


# Subscript expressions

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
element = matrix[row_idx][col_idx]
slice_result = matrix[start:end:step]

result = (very_long_array_name[first_complex_index][second_complex_index][third_complex_index]['key1']['key2']['key3'])


# Long expressions with multiple dots

result = (very_long_object_name.with_some_method_call().chain_another_method().and_another_method_with_args(arg1, arg2).final_method())


# Arithmetic and logical operators

result = (
    first_long_variable_name * second_long_variable_name +
    third_long_variable_name / fourth_long_variable_name)

condition = (
    first_condition and second_condition or
    third_condition and fourth_condition)


# Comments and spacing

def function_with_comments(arg1, # First argument
    arg2, # Second argument
    arg3  # Third argument
    ):
    # Function body
    pass


# Dataclass with field definitions

@dataclass
class ConfigurationClass:
    name: str = field(default="default_name")
    value: Optional[int] = field(default=None, metadata={"description": "Some value"})
    items: list[str] = field(default_factory=list)


# Function with local imports

def function_with_local_imports(data: Any) -> dict:
    """Process data using locally imported utilities."""
    from collections import defaultdict
    from itertools import groupby
    from operator import itemgetter
    import numpy as np
    from pandas import DataFrame
    from scipy.stats import zscore
    from emcd_testpkg.utils import process_data
    from emcd_testpkg.validation import validate_input

    # Function implementation...
    pass
