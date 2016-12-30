# vim:fileencoding=UTF-8 
#
# Copyright © 2015, 2016 Stan Livitski
#     
#  This file is part of EPyColl. EPyColl is
#  Licensed under the Apache License, Version 2.0 with modifications,
#  (the "License"); you may not use this file except in compliance
#  with the License. You may obtain a copy of the License at
#
#  https://raw.githubusercontent.com/StanLivitski/EPyColl/master/LICENSE
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
"""
    Structures and tools that help maintain mappings between objects.
    
    Helper classes and utility functions for establishing object
    mappings in addition to the functionality of the built-in
    dictionary class.

    Key elements
    ------------
    ImmutableMap : A wrapper class for a mapping that makes it
    immutable.
    OneToOneMap : A reversible dictionary class for one-to-one
    mapping between keys and values.
    IReversibleMap : An interface that describes a reversible
    dictionary.
 
"""

import version

version.requirePythonVersion(3)

import abc
import collections

class IReversibleMap(collections.Mapping, metaclass=abc.ABCMeta):
    """
    A protocol for mappings that define a reverse operation.
    
    In addition to all features of `collections.Mapping`, objects of
    this class define a `reverse` method that returns a mapping from
    values contained herein to their respective keys.
    
    Methods
    ---------------
    reverse()
        Reverse this mapping to map values to keys.

    See Also
    --------------
    OneToOneMap : An implementation of this class for one-to-one
    mappings.
    """

    @abc.abstractmethod    
    def reverse(self):
        """
        Reverse this mapping to map values to keys.
        
        Returns an object that maps values stored here to their
        respective keys. Note that returned object does not have to
        be of the same type as the one that returns it.
    
        Returns
        -------
        collections.Mapping
            a mapping container that maps this object's values to
            their keys. If the original mapping did not enforce unique
            values, reversed mapping may contain `Iterable`s over
            ambiguous keys in the original mapping. In cases where
            keys are themselves `Iterable`, implementors should wrap
            such keys in a singleton container. Subclasses that enforce
            unique values are exempt from this requirement.
        """
   
        raise NotImplemented()

class OneToOneMap(collections.MutableMapping, IReversibleMap):
    """
    A dictionary for one-to-one mapping between keys and values,
    with `reverse` method.
    
    A dictionary type that maintains strict one-to-one mapping
    between keys and values. Both keys and values must be immutable
    and implement `collections.Hashable`.
    
    Parameters
    --------------------
    mapping : collections.Mapping or iterable, optional
        A map or dictionary with initial mappings for this container,
        or a collection of name-value tuples representing such
        mappings. With no arguments, creates an empty container.

    Methods
    ---------------
    reverse()
        Reverse this mapping to map values to keys.

    Examples
    ----------------
    >>> outcomes = OneToOneMap()
    >>> print(outcomes)
    {}
    >>> outcomes or print("Ok")
    Ok
    >>> len(outcomes)
    0
    >>> outcomes==outcomes.reverse()
    True
    >>> outcomes is outcomes.reverse()
    False
    >>> outcomes['test']
    Traceback (most recent call last):
     ...
    KeyError: 'test'

    >>> outcomes['test']='positive'
    >>> outcomes['test']
    'positive'
    >>> outcomes.reverse()['positive']
    'test'
    >>> outcomes and print("Ok")
    Ok
    >>> len(outcomes)
    1
    >>> len(outcomes.reverse())
    1
    >>> outcomes==outcomes.reverse()
    False
    >>> print(outcomes)
    {'test': 'positive'}
    >>> print(outcomes.reverse())
    {'positive': 'test'}
    >>> del outcomes['test']
    >>> print(outcomes)
    {}

    >>> booleans = OneToOneMap([(0, False), (1, True)])
    >>> 0 in booleans
    True
    >>> 2 in booleans
    False
    >>> False in booleans.reverse()
    True
    >>> booleans.clear()
    >>> booleans
    OneToOneMap({})
    """

    def reverse(self):
        """
        Reverse this mapping to map values to keys.
        
        Returns a container of the same class that maps values inside
        this object's to their respective keys. 
    
        Returns
        -------
        OneToOneMap
            a mapping container that maps this object's values to
            their keys
    
        Examples
        --------
        >>> labels = OneToOneMap({'ten': '10'})
        >>> labels['deuce'] = '2'
        >>> labels.reverse().update(A='ace', K='king', Q='queen', J='jack')
        >>> print(sorted(labels.reverse().items()))
        [('10', 'ten'), ('2', 'deuce'), ('A', 'ace'), ('J', 'jack'), ('K', 'king'), ('Q', 'queen')]
        """
    
        return self._peer


    def __init__(self, mapping = None, _peer = None):
        if _peer is None:
            self._forward = {}
            self._reverse = {}
    
            if mapping is None:
                items = []
            elif isinstance(mapping, collections.Mapping):
                items = mapping.items()
            else:
                items = mapping
    
            for k, v in items:
                self[k] = v

            self._peer = OneToOneMap(_peer=self)
        else: # _peer is not None:
            self._peer = _peer
            self._forward = _peer._reverse
            self._reverse = _peer._forward

    def __str__(self):
        return str(self._forward)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    def __len__(self):
        len_ = len(self._forward)
        assert len(self._reverse) == len_, (
            'Forward mapping size differs from reverse mapping size',
            len_,
            len(self._reverse)
        )
        return len_

    def __getitem__(self, key):
        return self._forward[key]

    def __iter__(self):
        return iter(self._forward)

    def __contains__(self, item):
        return item in self._forward

    def __setitem__(self, key, value):
        if value in self._reverse and self._reverse[value] != key:
            # TODO: add an option of lenient forward mapping
            raise ValueError(
                value,
                'Value is already mapped to another key, please delete it before mapping to ' % key,
                self._reverse[value]
            )
        if key in self._forward and self._forward[key] != value:
            # TODO: add an option of lenient reverse mapping
            raise KeyError(
                key,
                'Key is already mapped to another value, please delete it before mapping to ' % value,
                self._forward[key]
            )
        self._forward[key] = value
        self._reverse[value] = key

    def __delitem__(self, key):
        value = self._forward[key]
        del self._reverse[value]
        del self._forward[key]

# TODO: make objects of this class Hashable
class ImmutableMap(IReversibleMap):
    """
    Wrapper around a mapping that makes it immutable.
    
    Wraps a mapping object to make it immutable. Since any direct
    references to the underlying object allow you to change its
    contents, you should destroy all such references after creating
    the wrapper to achieve true immutability.
    
    Parameters
    ----------
    mapping : collections.Mapping
        the underlying mapping

    Methods
    ---------------
    reverse()
        Reverse this mapping to map values to keys, if the underlying
        mapping is an `IReversibleMap`.
 
    Examples
    --------
    >>> map = ImmutableMap({'access': 'code'})
    >>> len(map)
    1
    >>> map['access']
    'code'
    >>> 'code' in map
    False
    >>> map['monkey']='wrench'
    Traceback (most recent call last):
    ...
    TypeError: 'ImmutableMap' object does not support item assignment
    >>> len(map)
    1
    >>> del map['access']
    Traceback (most recent call last):
    ...
    TypeError: 'ImmutableMap' object does not support item deletion
    >>> len(map)
    1
    >>> map.reverse()
    Traceback (most recent call last):
    ...
    TypeError: Mapping of type 'dict' is not reversible
    """
    def _readOnlyAttr(self, name, *value):
        if name in {'_mapping', '_reverse'}:
            raise AttributeError(name + " is a read-only attribute")
        elif 0 < len(value):
            super(ImmutableMap, self).__setattr__(name, *value)
        else:
            super(ImmutableMap, self).__delattr__(name)

    __setattr__ = _readOnlyAttr
    __delattr__ = _readOnlyAttr

    def __init__(self, mapping):
        if not isinstance(mapping, collections.Mapping):
            raise TypeError("Wrapped object of a non-mapping type: " + type(mapping).__name__)
        self.__dict__['_mapping'] = mapping
        self.__dict__['_reverse'] = None

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def __getitem__(self, key):
        return self._mapping[key]

    def __contains__(self, item):
        return item in self._mapping

    def __str__(self):
        return str(self._mapping)

    def __repr__(self):
        return 'ImmutableMap(%s)' % self._mapping

    def keys(self):
        return self._mapping.keys()

    def items(self):
        return self._mapping.items()

    def values(self):
        return self._mapping.values()

    def reverse(self):
        """
        Return the reverse mapping if the wrapped object supports that.
        
        This method requires that the wrapped object must also be
        reversible. 
    
        Returns
        -------
        collections.Mapping
            Immutable wrapper around the reverse mapping. Returned wrapper
            is always reversible, and its reverse version is this object.
    
        Raises
        ------
        TypeError
            If the wrapped object is not reversible.
    
        Examples
        --------
        >>> oneone  = ImmutableMap(OneToOneMap({1: "one"}))
        >>> print(oneone.reverse())
        {'one': 1}
        >>> oneone.reverse()['two']=2
        Traceback (most recent call last):
        ...
        TypeError: 'ImmutableMap' object does not support item assignment
        >>> oneone.reverse().reverse() is oneone
        True
        """
        
        if self._reverse is None:     
            if not isinstance(self._mapping, IReversibleMap):
                raise TypeError("Mapping of type '%s' is not reversible" % type(self._mapping).__name__)
            self.__dict__['_reverse'] = ImmutableMap(self._mapping.reverse())
            self._reverse.__dict__['_reverse'] = self
        return self._reverse

if __name__ == "__main__":
    import doctest
    doctest.testmod()
