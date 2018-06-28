# -*- coding: utf-8 -*-

# This file is part of 'nark'.
#
# 'nark' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'nark' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'nark'. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, unicode_literals

from collections import namedtuple

from future.utils import python_2_unicode_compatible
from six import text_type

from .item_base import BaseItem


CategoryTuple = namedtuple(
    'CategoryTuple', ('pk', 'name', 'deleted', 'hidden'),
)


@python_2_unicode_compatible
class Category(BaseItem):
    """Storage agnostic class for categories."""

    def __init__(self, name, pk=None, deleted=False, hidden=False):
        """
        Initialize this instance.

        Args:
            name (str): The name of the category. May contain whitespace!
            pk: The unique primary key used by the backend.
        """

        super(Category, self).__init__(pk, name)
        self.deleted = bool(deleted)
        self.hidden = bool(hidden)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError(_("You need to specify a Category name."))
        self._name = text_type(name)

    def as_tuple(self, include_pk=True):
        """
        Provide a tuple representation of this categories relevant 'fields'.

        Args:
            include_pk (bool): Whether to include the instances pk or not. Note that if
            ``False`` ``tuple.pk = False``!

        Returns:
            CategoryTuple: Representing this categories values.
        """
        pk = self.pk
        if not include_pk:
            pk = False
        cat_tup = CategoryTuple(
            pk=pk, name=self.name, deleted=self.deleted, hidden=self.hidden,
        )
        return cat_tup

    def equal_fields(self, other):
        """
        Compare this instances fields with another category.
        This excludes comparing the PK.

        Args:
            other (Category): Category to compare this instance with.

        Returns:
            bool: ``True`` if all fields but ``pk`` are equal, ``False`` if not.

        Note:
            This is particularly useful if you want to compare a new
            ``Category`` instance with a freshly created backend instance. As
            the latter will probably have a primary key assigned now and so
            ``__eq__`` would fail.
        """
        if other:
            other = other.as_tuple(include_pk=False)
        else:
            other = None

        return self.as_tuple(include_pk=False) == other

    def __eq__(self, other):
        if other is not None and not isinstance(other, CategoryTuple):
            other = other.as_tuple()
        return self.as_tuple() == other

    def __hash__(self):
        """Naive hashing method."""
        return hash(self.as_tuple())

    def __str__(self):
        return text_type('{name}'.format(name=self.name))

    def __repr__(self):
        """Return an instance representation containing additional information."""
        return str('[{pk}] {name}'.format(pk=repr(self.pk), name=repr(self.name)))

