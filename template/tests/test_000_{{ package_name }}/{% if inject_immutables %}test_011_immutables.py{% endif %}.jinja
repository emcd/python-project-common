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


''' Assert correct function of immutables. '''


from platform import python_implementation

import pytest

from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.__.immutables"
THESE_CLASSES_NAMES = ( 'ImmutableClass', )

pypy_skip_mark = pytest.mark.skipif(
    'PyPy' == python_implementation( ),
    reason = "PyPy handles class cell updates differently" )


def test_100_concealer_instantiation( ):
    ''' Concealer extension class instantiates. '''
    module = cache_import_module( MODULE_QNAME )
    obj = module.ConcealerExtension( )
    assert isinstance( obj, module.ConcealerExtension )
    assert hasattr( obj, '_attribute_visibility_includes_' )


def test_110_concealer_visibility( ):
    ''' Concealer extension class conceals attributes according to rules. '''
    module = cache_import_module( MODULE_QNAME )

    class Example( module.ConcealerExtension ):
        _attribute_visibility_includes_ = frozenset( ( '_visible', ) )

    obj = Example( )
    obj.public = 42
    obj._hidden = 24
    obj._visible = 12
    assert ( '_visible', 'public' ) == tuple( sorted( dir( obj ) ) )


@pytest.mark.parametrize( 'class_name', THESE_CLASSES_NAMES )
def test_200_immutable_class_init( class_name ):
    ''' Class prevents modification after initialization. '''
    module = cache_import_module( MODULE_QNAME )
    factory = getattr( module, class_name )

    class Example( metaclass = factory ):
        value = 42

    with pytest.raises( AttributeError ): Example.value = 24
    with pytest.raises( AttributeError ): del Example.value


@pytest.mark.parametrize( 'class_name', THESE_CLASSES_NAMES )
def test_210_immutable_class_visibility( class_name ):
    ''' Class conceals attributes according to rules. '''
    module = cache_import_module( MODULE_QNAME )
    factory = getattr( module, class_name )

    class Example( metaclass = factory ):
        _class_behaviors_ = { 'foobar' }
        _class_attribute_visibility_includes_ = frozenset( ( '_visible', ) )
        public = 42
        _hidden = 24
        _visible = 12

    assert ( '_visible', 'public' ) == tuple( sorted( dir( Example ) ) )


@pypy_skip_mark
@pytest.mark.parametrize( 'class_name', THESE_CLASSES_NAMES )
def test_220_immutable_class_decorators( class_name ):
    ''' Class handles decorators correctly. '''
    from dataclasses import dataclass
    module = cache_import_module( MODULE_QNAME )
    factory = getattr( module, class_name )

    def add_attr( cls ):
        cls.added = 'value'
        return cls

    class Example(
        metaclass = factory,
        decorators = ( dataclass( slots = True ), add_attr )
    ):
        field: str = 'test'

    assert hasattr( Example, '__slots__' )
    assert 'value' == Example.added
    with pytest.raises( AttributeError ): Example.added = 'changed'


@pypy_skip_mark
def test_221_immutable_class_replacement_super_method( ):
    ''' ImmutableClass handles class replacement by decorators. '''
    from dataclasses import dataclass
    module = cache_import_module( MODULE_QNAME )
    factory = module.ImmutableClass

    class Example(
        metaclass = factory,
        decorators = ( dataclass( slots = True ), )
    ):
        field1: str
        field2: int

        def method_with_super( self ):
            ''' References class cell on CPython. '''
            super( ).__init__( )
            return self.__class__.__name__

    obj = Example( field1 = 'test', field2 = 42 )
    assert 'Example' == obj.method_with_super( )
    assert hasattr( Example, '__slots__' )
    with pytest.raises( AttributeError ):
        Example.field1 = 'changed'


@pypy_skip_mark
def test_222_immutable_class_replacement_super_property( ):
    ''' ImmutableClass handles class replacement by decorators. '''
    from dataclasses import dataclass
    module = cache_import_module( MODULE_QNAME )
    factory = module.ImmutableClass

    class Example(
        metaclass = factory,
        decorators = ( dataclass( slots = True ), )
    ):
        field1: str
        field2: int

        @property
        def prop_with_class( self ):
            ''' References class cell on CPython. '''
            return self.__class__.__name__

    obj = Example( field1 = 'test', field2 = 42 )
    assert 'Example' == obj.prop_with_class
    assert hasattr( Example, '__slots__' )
    with pytest.raises( AttributeError ):
        Example.field1 = 'changed'


# pylint: disable=no-member

def test_300_module_reclassification_by_name( ):
    ''' Module reclassification works with module name. '''
    module = cache_import_module( MODULE_QNAME )
    from types import ModuleType
    test_module = ModuleType( f"{PACKAGE_NAME}.test" )
    test_module.__package__ = PACKAGE_NAME
    from sys import modules
    modules[ test_module.__name__ ] = test_module
    module.reclassify_modules( test_module.__name__ )
    assert isinstance( test_module, module.ImmutableModule )
    with pytest.raises( AttributeError ):
        test_module.new_attr = 42


def test_301_module_reclassification_by_object( ):
    ''' Module reclassification works with module object. '''
    module = cache_import_module( MODULE_QNAME )
    from types import ModuleType
    test_module = ModuleType( f"{PACKAGE_NAME}.test" )
    test_module.__package__ = PACKAGE_NAME
    module.reclassify_modules( test_module )
    assert isinstance( test_module, module.ImmutableModule )
    with pytest.raises( AttributeError ):
        test_module.new_attr = 42


def test_302_recursive_module_reclassification( ):
    ''' Recursive module reclassification works. '''
    module = cache_import_module( MODULE_QNAME )
    from types import ModuleType
    root = ModuleType( f"{PACKAGE_NAME}.test" )
    root.__package__ = PACKAGE_NAME
    sub1 = ModuleType( f"{PACKAGE_NAME}.test.sub1" )
    sub2 = ModuleType( f"{PACKAGE_NAME}.test.sub2" )
    root.sub1 = sub1
    root.sub2 = sub2
    module.reclassify_modules( root, recursive = True )
    assert isinstance( root, module.ImmutableModule )
    assert isinstance( sub1, module.ImmutableModule )
    assert isinstance( sub2, module.ImmutableModule )
    with pytest.raises( AttributeError ):
        root.new_attr = 42
    with pytest.raises( AttributeError ):
        sub1.new_attr = 42
    with pytest.raises( AttributeError ):
        sub2.new_attr = 42


def test_303_module_reclassification_respects_package( ):
    ''' Module reclassification only affects package modules. '''
    module = cache_import_module( MODULE_QNAME )
    from types import ModuleType
    root = ModuleType( f"{PACKAGE_NAME}.test" )
    root.__package__ = PACKAGE_NAME
    external = ModuleType( "other_package.module" )
    other_pkg = ModuleType( "other_package" )
    root.external = external
    root.other_pkg = other_pkg
    module.reclassify_modules( root, recursive = True )
    assert isinstance( root, module.ImmutableModule )
    assert not isinstance( external, module.ImmutableModule )
    assert not isinstance( other_pkg, module.ImmutableModule )
    with pytest.raises( AttributeError ):
        root.new_attr = 42
    external.new_attr = 42  # Should work
    assert 42 == external.new_attr


def test_304_module_reclassification_by_dict( ):
    ''' Module reclassification works with attribute dictionary. '''
    module = cache_import_module( MODULE_QNAME )
    from types import ModuleType
    m1 = ModuleType( f"{PACKAGE_NAME}.test1" )
    m2 = ModuleType( f"{PACKAGE_NAME}.test2" )
    m3 = ModuleType( "other.module" )
    attrs = {
        '__package__': PACKAGE_NAME,
        'module1': m1,
        'module2': m2,
        'external': m3,
        'other': 42,
    }
    module.reclassify_modules( attrs )
    assert isinstance( m1, module.ImmutableModule )
    assert isinstance( m2, module.ImmutableModule )
    assert not isinstance( m3, module.ImmutableModule )
    with pytest.raises( AttributeError ):
        m1.new_attr = 42
    with pytest.raises( AttributeError ):
        m2.new_attr = 42
    m3.new_attr = 42  # Should work


def test_305_module_reclassification_requires_package( ):
    ''' Module reclassification requires package name. '''
    module = cache_import_module( MODULE_QNAME )
    from types import ModuleType
    m1 = ModuleType( f"{PACKAGE_NAME}.test1" )
    attrs = { 'module1': m1 }
    module.reclassify_modules( attrs )
    assert not isinstance( m1, module.ImmutableModule )
    m1.new_attr = 42
    assert 42 == m1.new_attr


def test_306_module_attribute_operations( ):
    ''' Module prevents attribute deletion and modification. '''
    module = cache_import_module( MODULE_QNAME )
    from types import ModuleType
    test_module = ModuleType( f"{PACKAGE_NAME}.test" )
    test_module.__package__ = PACKAGE_NAME
    test_module.existing = 42
    module.reclassify_modules( test_module )
    with pytest.raises( AttributeError ) as exc_info:
        del test_module.existing
    assert "Cannot delete attribute 'existing'" in str( exc_info.value )
    assert test_module.__name__ in str( exc_info.value )
    with pytest.raises( AttributeError ) as exc_info:
        test_module.existing = 24
    assert "Cannot assign attribute 'existing'" in str( exc_info.value )
    assert test_module.__name__ in str( exc_info.value )
    assert 42 == test_module.existing

# pylint: enable=no-member


def test_400_immutable_object_init( ):
    ''' Object prevents modification after initialization. '''
    module = cache_import_module( MODULE_QNAME )

    class Example( module.ImmutableObject ):
        def __init__( self ):
            super( module.ImmutableObject, self ).__setattr__( 'value', 42 )
            super( ).__init__( )

    obj = Example( )
    with pytest.raises( AttributeError ): obj.value = 24
    with pytest.raises( AttributeError ): obj.new_attr = 'test'
    with pytest.raises( AttributeError ): del obj.value


def test_500_name_calculation( ):
    ''' Name calculation functions work correctly. '''
    module = cache_import_module( MODULE_QNAME )
    assert 'builtins.NoneType' == module.calculate_fqname( None )
    assert (
        'builtins.type'
        == module.calculate_fqname( module.ConcealerExtension ) )


@pytest.mark.parametrize(
    'provided, expected',
    (
        ( { 'foo': 12 }, ( ) ),
        ( { '_foo': cache_import_module }, ( ) ),
        (
            { 'public_func': lambda: None },
            ( 'public_func', )
        ),
    )
)
def test_600_attribute_discovery( provided, expected ):
    ''' Public attributes are discovered from dictionary. '''
    module = cache_import_module( MODULE_QNAME )
    assert expected == module.discover_public_attributes( provided )
