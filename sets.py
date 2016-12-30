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
    Structures that implement the `collections.Set` protocol
    to store sets of unique items.
    
    This module provides implementations of `collections.Set`
    with features missing from the collections library,
    such as sorted sets.

    Key elements
    ------------
    SortedListSet : Implementation of `collections.Set` backed by
    a sorted list.

"""

import version

version.requirePythonVersion(3)

import collections
import math

class SortedListSet(collections.MutableSet):
    """
    Implementation of `collections.Set` backed by a sorted list.
    
    A `collections.Set` that returns elements in the ascending
    sort order when iterated. The sort order can be defined using
    a key function when the set is created. This class uses a sorted
    list to store its elements. Its instances have linear complexity
    when adding or deleting elements at random or iterating over contents,
    and logarithmic complexity when looking up an element or adding
    elements to the end of the set.
    
    Parameters
    --------------------
    key : object, optional
        A callable object, such as a function, that takes one argument
        used to extract a comparison key from each set element, e.g.
        key=str.lower. This function should return different values for
        inequal elements. Otherwise, an element added to the set with a
        key equal to that of an existing element shall replace that
        element. The default value is None (compare the elements directly).
    iterable : Iterable, optional
        A collection to take initial elements of this set from.

    Attributes
    -----------------
    modCount : int
        The number of times this set has been changed since creation.
        This is used to invalidate iterators when a change is made to the
        set. You should not modify this attribute directly unless you
        bypass this class's methods to manipulate the set.  

    Methods
    ---------------
    iter(from, to)
        Return an iterator over a subset limited by argument values.

    Raises
    ----------
    ValueError
        If the iterable argument reports a size that differs from its
        actual number of elements.
    TypeError
        If the key argument is not callable.

[    See Also
    --------------
    <python_name> : <Description of code referred by this line
    and how it is related to the documented code.>
     ... ]

    Examples
    ----------------
    >>> s=SortedListSet()
    >>> str(s)
    '()'
    >>> len(s)
    0
    >>> s.add(1)
    >>> s
    SortedListSet({1})
    >>> s |= ('foo', 'bar')
    Traceback (most recent call last):
    ...
    TypeError: unorderable types: int() > str()
    >>> s |= (0, 15, 1, -3)
    >>> len(s)
    4
    >>> s.remove(1)
    >>> print(s)
    {-3, 0, 15}
    >>> s=SortedListSet('ABrACadEbra', key=str.lower)
    >>> s
    SortedListSet({'a', 'b', 'C', 'd', 'E', 'r'})
    >>> 'e' in s
    False
    >>> 'f' in s
    False
    >>> 'E' in s
    True
    >>> all = SortedListSet('ABrACadEbra')
    >>> s <= all
    True
    >>> s1 = SortedListSet({'a', 'b', 'C', 'd', 'E', 'r'}, key=str.lower)
    >>> s1 == s
    True
    >>> s <= s1
    True
    >>> s <= SortedListSet('abCdEfqrZ', str.lower)
    True
    """

    def _readOnlyAttr(self, name, *value):
        if name in {'_key'}:
            raise AttributeError(name + " is a read-only attribute")
        elif 0 < len(value):
            super(SortedListSet, self).__setattr__(name, *value)
        else:
            super(SortedListSet, self).__delattr__(name)

    __setattr__ = _readOnlyAttr
    __delattr__ = _readOnlyAttr

    def __init__(self, iterable = None, key = None):
        self.__dict__['_key'] = key if key is not None else (lambda x: x)
        if '__call__' not in dir(self._key):
            raise TypeError(
                'key argument is of a non-callable %s'
                % type(key)
            )
        self.__dict__['_list'] = [ None ] * len(iterable) if isinstance(iterable, collections.Sized) else []
        if isinstance(iterable, collections.Sized):
            i = 0
            for item in iterable:
                self._list[i] = item
                i += 1
            if len(self._list) > i:
                raise ValueError(
                    'argument collection reported incorrect size %d, actual element count was %d'
                    % ( len(self._list), i )
                )
        elif iterable is not None:
            for item in iterable:
                self._list.append(item)
        self._list.sort(key = self._key)
        if self._list:
            last = self._list[0]
            i = 1
            while i < len(self._list):
                if self._key(last) == self._key(self._list[i]):
                    i -= 1
                    del self._list[i]
                last = self._list[i]
                i += 1
        self.modCount = 0

    def __str__(self):
        return '{' + ', '.join([ repr(e) for e in self ]) + '}' if self else '()'

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    def _pos(self, x, from_ = 0, to_ = None):
        """
        Return the position of specified element in the underlying list,
        or the position it should be inserted at to maintain the list's order.
        """
        if to_ is None:
            to_ = len(self._list)
        key = self._key(x)
        while from_ < to_:
            at = (from_ + to_) >> 1
            pivot = self._key(self._list[at])
            if pivot == key:
                from_ = at
                break
            elif pivot > key:
                to_ = at
            else:
                from_ = at + 1
        return from_

    def __contains__(self, x):
        at = self._pos(x)
        return len(self._list) > at and self._list[at] == x

    def add(self, value):
        at = self._pos(value)
        if len(self._list) <= at:
            self._list.append(value)
        elif self._key(value) == self._key(self._list[at]):
            if self._list[at] == value:
                return # set is not modified
            self.modCount += 1
            self._list[at] = value
        else:
            self.modCount += 1
            self._list.insert(at, value)

    def discard(self, value):
        at = self._pos(value)
        if len(self._list) > at and self._list[at] == value:
            self.modCount += 1
            del self._list[at]

    _log2base = math.log(2)

    def __le__(self, other):
        if not isinstance(other, SortedListSet):
            return collections.MutableSet.__le__(self, other)
        len_ = len(self._list)
        olen = len(other._list)
        if len_ > olen:
            return False
        elif 100 < olen and 2 * len_ * math.log(olen) / self._log2base < olen or self._key != other._key:
            # No  linear scan possible, or no performance gain, fall back to the library
            return collections.MutableSet.__le__(self, other)
        i = 0
        for item in self._list:
            if item == other._list[i]:
                i += 1
                continue
            else:
                mykey = self._key(item)
                otherkey = self._key(other._list[i])
                if mykey <= otherkey:
                    return False
                i += 1
                while i < len(other._list):
                    if mykey > self._key(other._list[i]):
                        i += 1 
                    else:
                        break
                if i >= len(other._list):
                    return False
        return True

    def __eq__(self, other):
        if not isinstance(other, SortedListSet) or self._key != other._key:
            return collections.MutableSet.__le__(self, other)
        len_ = len(self._list)
        if len_ != len(other._list):
            return False
        for i in range(0, len_):
            if self._list[i] != other._list[i]:
                return False
        return True

    def __iter__(self):
        return self.iter()

    def __len__(self):
        return len(self._list)

    def iter(self, from_ = None, to_ = None):
        """
        Return an iterator over a subset limited by argument values.
        
        Limits this set to values that fall within specified
        boundaries and returns an iterator over matching elements.
        
        Parameters
        ----------
        from_ : object, optional
            A value that begins or precedes requested iteration range.
            If present in the set, this value will be returned by the
            iterator. Default is None, which means start of the set's
            value range.
        to_ : object, optional
            A value that follows requested iteration range. If present
            in the set, this value will be omitted by the iterator.
            Default is None, which means past end of the set's value
            range.
    
        Returns
        -------
        SortedListSetIterator
            Iterator over a subset limited by argument values valid
            until the next modification of this set.
    
        Examples
        --------
        >>> s=SortedListSet(key=str.lower)
        >>> s |= 'DEBArcADEro'
        >>> s
        SortedListSet({'A', 'B', 'c', 'D', 'E', 'o', 'r'})
        >>> [ i for i in s.iter('f', 'r') ]
        ['o']
        >>> [ i for i in s.iter(to_ = 'f') ]
        ['A', 'B', 'c', 'D', 'E']
        >>> [ i for i in s.iter(to_ = 'e') ]
        ['A', 'B', 'c', 'D']
        >>> [ i for i in s.iter(from_ = 'e') ]
        ['E', 'o', 'r']
        >>> [ i for i in s.iter(from_ = 's') ]
        []
        """
    
        fromIndex = 0 if from_ is None else self._pos(from_)
        toIndex = len(self._list) if to_ is None else self._pos(to_)
        return self.Iterator(self, fromIndex, toIndex)

    class Iterator(collections.Iterator):
    
        def __init__(self, set_, from_, to_):
            self._modCount = set_.modCount
            self._set = set_
            self._iter = iter(set_._list[from_: to_])
    
        def __next__(self):
            if self._modCount != self._set.modCount:
                raise RuntimeError('set %s has been modified during the iteration' % self._set)
            return self._iter.__next__()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
