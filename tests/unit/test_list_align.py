# -*- coding: utf-8 -*-
#
# This file is part of Inspirehep.
# Copyright (C) 2016 CERN.
#
# Inspirehep is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Inspirehep is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Inspirehep; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Acceptance scenarios for the merger."""

from __future__ import absolute_import, print_function

import pytest

from json_merger.errors import MergeError
from json_merger.list_unify import ListUnifier, UnifierOps
from json_merger.nothing import NOTHING


def test_value_error():
    with pytest.raises(ValueError):
        ListUnifier([], [], [], 'BAD_OPERATION')


def test_keep_only_head_entitites():
    root = [1, 2]
    head = [1, 2, 3]
    update = [6, 5, 4, 3, 2]

    u = ListUnifier(root, head, update, UnifierOps.KEEP_ONLY_HEAD_ENTITIES)
    u.unify()

    assert u.unified == [(1, 1, NOTHING), (2, 2, 2), (NOTHING, 3, 3)]


def test_keep_only_update_entities():
    root = [1, 2]
    head = [6, 5, 4, 3, 2]
    update = [1, 2, 3]

    u = ListUnifier(root, head, update, UnifierOps.KEEP_ONLY_UPDATE_ENTITIES)
    u.unify()

    assert u.unified == [(1, NOTHING, 1), (2, 2, 2), (NOTHING, 3, 3)]


def test_keep_update_and_head_ent_head_fst():
    root = [1, 2]
    head = [5, 4, 3, 2]
    update = [10, 3, 1, 2, 11]

    u = ListUnifier(root, head, update,
                    UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST)
    u.unify()

    assert u.unified == [(NOTHING, 5, NOTHING), (NOTHING, 4, NOTHING),
                         (NOTHING, NOTHING, 10),
                         (NOTHING, 3, 3), (1, NOTHING, 1),
                         (2, 2, 2),
                         (NOTHING, NOTHING, 11)]


def test_keep_update_and_head_ent_update_fst():
    root = [1, 2]
    head = [5, 4, 3, 2]
    update = [10, 3, 1, 2, 11]

    u = ListUnifier(root, head, update,
                    UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST)
    u.unify()

    assert u.unified == [(NOTHING, NOTHING, 10),
                         (NOTHING, 5, NOTHING), (NOTHING, 4, NOTHING),
                         (NOTHING, 3, 3), (1, NOTHING, 1),
                         (2, 2, 2),
                         (NOTHING, NOTHING, 11)]


def test_keep_update_and_head_ent_head_fst_fallback():
    root = [1, 2]
    head = [1, 2, 3]
    update = [7, 3, 6, 1, 5, 2, 4]

    u = ListUnifier(root, head, update,
                    UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST)

    with pytest.raises(MergeError):
        u.unify()

    assert u.unified == [(1, 1, 1), (2, 2, 2), (NOTHING, 3, 3),
                         (NOTHING, NOTHING, 7),
                         (NOTHING, NOTHING, 6),
                         (NOTHING, NOTHING, 5),
                         (NOTHING, NOTHING, 4)]


def test_error_on_head_delete():
    root = [1, 2]
    head = [1, 2, 3]
    update = [1, 2, 4]

    u = ListUnifier(root, head, update,
                    UnifierOps.KEEP_UPDATE_ENTITIES_CONFLICT_ON_HEAD_DELETE)

    with pytest.raises(MergeError):
        u.unify()
