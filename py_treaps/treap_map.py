from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast

from py_treaps.treap import KT, VT, Treap
from py_treaps.treap_node import TreapNode


# Example usage found in test_treaps.py
class TreapMap(Treap[KT, VT]):
    # Add an __init__ if you want. Make the parameters optional, though.
    def __init__(self):
        self.root = None

    def get_root_node(self) -> Optional[TreapNode]:
        return self.root

    def lookup(self, key: KT) -> Optional[VT]:
        if self.get_root_node() is None:
            return None
        node = self.lookup_helper(self.get_root_node(), key)
        if node is not None:
            return node.value
        else:
            return None

    def shifter_heap(self):
        self.shifter_heap_help(self.get_root_node())

    def shifter_heap_help(self, node):
        if node is None:
            return
        if node.left_child is not None and node.right_child is not None:
            if node.left_child.priority > node.priority and node.left_child.priority > node.right_child.priority:
                self.rotate_right(node)
                return
            elif node.right_child.priority > node.priority and node.right_child.priority > node.left_child.priority:
                self.rotate_left(node)
                return
        elif node.left_child is not None:
            if node.left_child.priority > node.priority:
                self.rotate_right(node)
                return
        elif node.right_child is not None:
            if node.right_child.priority > node.priority:
                self.rotate_left(node)
                return
        self.shifter_heap_help(node.left_child)
        self.shifter_heap_help(node.right_child)

    def shifter_bst(self):
        self.shifter_bst_help(self.get_root_node())

    def shifter_bst_help(self, node):
        if node is None:
            return
        elif node.left_child is not None:
            if node.left_child.key > node.key:
                self.rotate_right(node)
                return
        elif node.right_child is not None:
            if node.right_child.key < node.key:
                self.rotate_left(node)
                return
        self.shifter_bst_help(node.left_child)
        self.shifter_bst_help(node.right_child)

    def lookup_helper(self, node, key):
        if node.key == key:
            return node
        elif key > node.key:
            if node.right_child is None:
                return None
            return self.lookup_helper(node.right_child, key)
        elif key < node.key:
            if node.left_child is None:
                return None
            return self.lookup_helper(node.left_child, key)

    def insert(self, key: KT, value: VT):
        if self.get_root_node() is None:
            self.root = TreapNode(key, value)
        else:
            self.insert_helper(key, value, self.get_root_node())

        while not(self.BST_check() and self.heap_check()):
            self.shifter_bst()
            self.shifter_heap()

    def insert_helper(self, key: KT, value: VT, node) -> None:
        if node.key == key:
            node.value = value
        elif key < node.key:
            if node.left_child is None:
                node.left_child = TreapNode(key, value)
                node.left_child.parent = node
            else:
                self.insert_helper(key, value, node.left_child)
        elif key > node.key:
            if node.right_child is None:
                node.right_child = TreapNode(key, value)
                node.right_child.parent = node
            else:
                self.insert_helper(key, value, node.right_child)

    def rotate_right(self, node):  # giving top node
        new_node = node.left_child
        if new_node.right_child is not None:
            node.left_child = new_node.right_child
            node.left_child.parent = node
        else:
            if self.get_root_node() == node:
                self.root = new_node
            node.left_child = None
        if node.parent is not None:
            if node.parent.left_child == node:
                node.parent.left_child = new_node
            elif node.parent.right_child == node:
                node.parent.right_child = new_node
        new_node.right_child = node
        new_node.parent = node.parent
        node.parent = new_node
        if new_node.parent is None:
            self.root = new_node

    def rotate_left(self, node):
        new_node = node.right_child
        if new_node.left_child is not None:
            node.right_child = new_node.left_child
            node.right_child.parent = node
        else:
            if self.get_root_node() == node:
                self.root = new_node
            node.right_child = None
        if node.parent is not None:
            if node.parent.left_child == node:
                node.parent.left_child = new_node
            elif node.parent.right_child == node:
                node.parent.right_child = new_node
        new_node.left_child = node
        new_node.parent = node.parent
        node.parent = new_node
        if new_node.parent is None:
            self.root = new_node


    def BST_check(self):
        return self.is_bst_helper(self.get_root_node(), min(self.__iter__()), max(self.__iter__()))

    def is_bst_helper(self, node, min_key, max_key):
        if node is None:
            return True

        if not (min_key <= node.key <= max_key):
            return False

        left_valid = self.is_bst_helper(node.left_child, min_key, node.key)
        right_valid = self.is_bst_helper(node.right_child, node.key, max_key)

        return left_valid and right_valid

    def heap_check(self):
        if self.get_root_node() is None:
            return True
        else:
            return self.heap_check_helper(self.get_root_node())

    def heap_check_helper(self, node):
        if node is None:
            return True
        if node.left_child is not None and node.left_child.priority > node.priority:
            return False
        if node.right_child is not None and node.right_child.priority > node.priority:
            return False
        return self.heap_check_helper(node.left_child) and self.heap_check_helper(node.right_child)

    def remove(self, key: KT) -> Optional[VT]:
        value = None
        if self.get_root_node() is None:
            return value
        if self.get_root_node().left_child is None and self.get_root_node().right_child is None:
            self.root = None
            return self.get_root_node().value
        else:
            node = self.lookup_helper(self.get_root_node(), key)
            value = node.value
            self.remover_help(node)
        while not (self.BST_check() and self.heap_check()):
            self.shifter_bst()
            self.shifter_heap()
        return value

    def remover_help(self, node):
        if node.left_child is None and node.right_child is None:
            value = node.value
            if node.parent.left_child == node:
                node.parent.left_child = None
                node.parent = None
                return value
            elif node.parent.right_child == node:
                node.parent.right_child = None
                node.parent = None
                return value
        elif node.right_child is not None and node.left_child is not None:
            if node.right_child.priority > node.left_child.priority:
                self.rotate_left(node)
            else:
                self.rotate_right(node)
            self.remover_help(node)
        elif node.right_child is None and node.left_child is not None:
            self.rotate_right(node)
            self.remover_help(node)
        elif node.left_child is None and node.right_child is not None:
            self.rotate_left(node)
            self.remover_help(node)

    def split(self, threshold: KT) -> List[Treap[KT, VT]]:
        less = []
        equal_more = []
        for key in self.__iter__():
            if key < threshold:
                less.append(key)
            else:
                equal_more.append(key)
        less_Tr = TreapMap()
        more_Tr = TreapMap()
        for key in less:
            less_Tr.insert(key, self.lookup(key))
        for key in equal_more:
            more_Tr.insert(key, self.lookup(key))
        return [less_Tr, more_Tr]

    def join(self, _other: Treap[KT, VT]) -> None:
        new_root = TreapNode(-1,5)
        new_root.left_child = self.get_root_node()
        new_root.right_child = _other.get_root_node()
        self.root = new_root
        self.remove(-1)


    def meld(self, other: Treap[KT, VT]) -> None:  # KARMA
        raise AttributeError

    def difference(self, other: Treap[KT, VT]) -> None:  # KARMA
        raise AttributeError

    def balance_factor(self) -> float:  # KARMA
        raise AttributeError

    def __str__(self):
        pass

    def __iter__(self) -> typing.Iterator[KT]:
        self.keys = []
        self.get_all_keys(self.get_root_node(), self.keys)
        self.keys.sort()
        self.iter = iter(self.keys)
        return self

    def get_all_keys(self, node, keys=None):
        if keys is None:
            keys = []
        if node is not None:
            self.get_all_keys(node.right_child, keys)
            keys.append(node.key)
            self.get_all_keys(node.left_child, keys)

    def __next__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopIteration
