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


''' Attribute concealment and immutability. '''


from __future__ import annotations

import collections.abc as cabc
import types

import typing_extensions as typx


ClassDecorators: typx.TypeAlias = (
    cabc.Iterable[ cabc.Callable[ [ type ], type ] ] )


behavior_label = 'immutability'


def repair_class_reproduction( original: type, reproduction: type ) -> None:
    ''' Repairs a class reproduction, if necessary. '''
    from platform import python_implementation
    match python_implementation( ):
        case 'CPython':  # pragma: no branch
            _repair_cpython_class_closures( original, reproduction )
        case _: pass  # pragma: no cover


def _repair_cpython_class_closures( # pylint: disable=too-complex
    original: type, reproduction: type
) -> None:
    # Adapted from https://github.com/python/cpython/pull/124455/files
    def try_repair_closure( function: cabc.Callable[ ..., typx.Any ] ) -> bool:
        try: index = function.__code__.co_freevars.index( '__class__' )
        except ValueError: return False
        if not function.__closure__: return False # pragma: no branch
        closure = function.__closure__[ index ]
        if original is closure.cell_contents: # pragma: no branch
            closure.cell_contents = reproduction
            return True
        return False # pragma: no cover

    from inspect import isfunction, unwrap
    for attribute in reproduction.__dict__.values( ): # pylint: disable=too-many-nested-blocks
        attribute_ = unwrap( attribute )
        if isfunction( attribute_ ) and try_repair_closure( attribute_ ):
            return
        if isinstance( attribute_, property ):
            for aname in ( 'fget', 'fset', 'fdel' ):
                accessor = getattr( attribute_, aname )
                if None is accessor: continue
                if try_repair_closure( accessor ): return # pragma: no branch


class ImmutableClass( type ):
    ''' Concealment and immutability on class attributes. '''

    _class_attribute_visibility_includes_: cabc.Collection[ str ] = (
        frozenset( ) )

    def __new__(
        clscls: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, typx.Any ], *,
        decorators: ClassDecorators = ( ),
        **args: typx.Any
    ) -> ImmutableClass:
        class_ = type.__new__( clscls, name, bases, namespace, **args )
        return _immutable_class__new__( class_, decorators = decorators )

    def __init__( selfclass, *posargs: typx.Any, **nomargs: typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _immutable_class__init__( selfclass )

    def __dir__( selfclass ) -> tuple[ str, ... ]:
        default: frozenset[ str ] = frozenset( )
        includes: frozenset[ str ] = frozenset.union( *( # type: ignore
            getattr( class_, '_class_attribute_visibility_includes_', default )
            for class_ in selfclass.__mro__ ) )
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if not name.startswith( '_' ) or name in includes ) )

    def __delattr__( selfclass, name: str ) -> None:
        if not _immutable_class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: typx.Any ) -> None:
        if not _immutable_class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )


def _immutable_class__new__(
    original: type,
    decorators: ClassDecorators = ( ),
) -> type:
    # Some decorators create new classes, which invokes this method again.
    # Short-circuit to prevent recursive decoration and other tangles.
    decorators_ = original.__dict__.get( '_class_decorators_', [ ] )
    if decorators_: return original
    setattr( original, '_class_decorators_', decorators_ )
    reproduction = original
    for decorator in decorators:
        decorators_.append( decorator )
        reproduction = decorator( original )
        if original is not reproduction:
            repair_class_reproduction( original, reproduction )
        original = reproduction
    decorators_.clear( )  # Flag '__init__' to enable immutability
    return reproduction


def _immutable_class__init__( class_: type ) -> None:
    # Some metaclasses add class attributes in '__init__' method.
    # So, we wait until last possible moment to set immutability.
    if class_.__dict__.get( '_class_decorators_' ): return
    del class_._class_decorators_
    if ( class_behaviors := class_.__dict__.get( '_class_behaviors_' ) ):
        class_behaviors.add( behavior_label )
    else: setattr( class_, '_class_behaviors_', { behavior_label } )


def _immutable_class__delattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    if behavior_label not in class_.__dict__.get(
        '_class_behaviors_', ( )
    ): return False
    raise AttributeError(
        "Cannot delete attribute {name!r} "
        "on class {class_fqname!r}.".format(
            name = name,
            class_fqname = calculate_class_fqname( class_ ) ) )


def _immutable_class__setattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    if behavior_label not in class_.__dict__.get(
        '_class_behaviors_', ( )
    ): return False
    raise AttributeError(
        "Cannot assign attribute {name!r} "
        "on class {class_fqname!r}.".format(
            name = name,
            class_fqname = calculate_class_fqname( class_ ) ) )


class ConcealerExtension:
    ''' Conceals instance attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _attribute_visibility_includes_: cabc.Collection[ str ] = frozenset( )

    def __dir__( self ) -> tuple[ str, ... ]:
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if not name.startswith( '_' )
                or name in self._attribute_visibility_includes_ ) )


class ImmutableModule(
    ConcealerExtension, types.ModuleType, metaclass = ImmutableClass
):
    ''' Concealment and immutability on module attributes. '''

    def __delattr__( self, name: str ) -> None:
        raise AttributeError( # noqa: TRY003
            f"Cannot delete attribute {name!r} "
            f"on module {self.__name__!r}." ) # pylint: disable=no-member

    def __setattr__( self, name: str, value: typx.Any ) -> None:
        raise AttributeError( # noqa: TRY003
            f"Cannot assign attribute {name!r} "
            f"on module {self.__name__!r}." ) # pylint: disable=no-member


class ImmutableObject( ConcealerExtension, metaclass = ImmutableClass ):
    ''' Concealment and immutability on instance attributes. '''

    def __delattr__( self, name: str ) -> None:
        raise AttributeError(
            "Cannot delete attribute {name!r} on instance "
            "of class {class_fqname!r}.".format(
                name = name, class_fqname = calculate_fqname( self ) ) )

    def __setattr__( self, name: str, value: typx.Any ) -> None:
        raise AttributeError(
            "Cannot assign attribute {name!r} on instance "
            "of class {class_fqname!r}.".format(
                name = name, class_fqname = calculate_fqname( self ) ) )


def calculate_class_fqname( class_: type ) -> str:
    ''' Calculates fully-qualified name for class. '''
    return f"{class_.__module__}.{class_.__qualname__}"


def calculate_fqname( obj: object ) -> str:
    ''' Calculates fully-qualified name for class of object. '''
    class_ = type( obj )
    return f"{class_.__module__}.{class_.__qualname__}"


def discover_public_attributes(
    attributes: cabc.Mapping[ str, typx.Any ]
) -> tuple[ str, ... ]:
    ''' Discovers public attributes of certain types from dictionary.

        By default, callables, including classes, are discovered.
    '''
    return tuple( sorted(
        name for name, attribute in attributes.items( )
        if not name.startswith( '_' ) and callable( attribute ) ) )

def reclassify_modules(
    attributes: typx.Annotated[
        cabc.Mapping[ str, typx.Any ] | types.ModuleType | str,
        typx.Doc( 'Module, module name, or dictionary of object attributes.' ),
    ],
    recursive: typx.Annotated[
        bool,
        typx.Doc( 'Recursively reclassify package modules?' ),
    ] = False,
) -> None:
    ''' Reclassifies modules to be immutable. '''
    from inspect import ismodule
    from sys import modules
    if isinstance( attributes, str ):
        attributes = modules[ attributes ]
    if isinstance( attributes, types.ModuleType ):
        module = attributes
        attributes = attributes.__dict__
    else: module = None
    package_name = (
        attributes.get( '__package__' ) or attributes.get( '__name__' ) )
    if not package_name: return
    for value in attributes.values( ):
        if not ismodule( value ): continue
        if not value.__name__.startswith( f"{package_name}." ): continue
        if recursive: reclassify_modules( value, recursive = True )
        if isinstance( value, ImmutableModule ): continue
        value.__class__ = ImmutableModule
    if module and not isinstance( module, ImmutableModule ):
        module.__class__ = ImmutableModule
