"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""

from __future__ import annotations
import os
from random import randint

from typing import Tuple, List, Optional


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    data_size: the total size of all leaves of this tree.
    colour: The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    _root: the root value of this tree, or None if this tree is empty.
    _subtrees: the subtrees of this tree.
    _parent_tree: the parent tree of this tree; i.e., the tree that contains
        this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    data_size: int
    colour: (int, int, int)
    _root: Optional[object]
    _subtrees: List[AbstractTree]
    _parent_tree: Optional[AbstractTree]

    def __init__(self: AbstractTree, root: Optional[object],
                 subtrees: List[AbstractTree], data_size: int = 0) -> None:
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self.data_size = data_size
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if not self._subtrees:
            self.data_size = data_size
        else:
            for tree in self._subtrees:
                self.data_size += tree.data_size
        for tree in self._subtrees:
            tree._parent_tree = self

    def is_empty(self: AbstractTree) -> bool:
        """Return True if this tree is empty."""
        return self._root is None

    def generate_treemap(self: AbstractTree, rect: Tuple[int, int, int, int])\
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        # Read the handout carefully to help get started identifying base cases,
        # and the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # coordinates of a rectangle, as follows.
        # x, y, width, height = rect
        tree = []
        if self.data_size == 0:
            return []
        if not self._subtrees:
            return [(rect, self.colour)]
        x, y, width, height = rect
        if width > height:
            tot_w = 0
            for subtree in self._subtrees:
                size = round(subtree.data_size / self.data_size, 2)
                w = round(width * size, 2)

                if subtree == self._subtrees[len(self._subtrees) - 1]:
                    tree.extend(subtree.generate_treemap((x, y, width - tot_w,
                                                          height)))
                else:
                    tree.extend(subtree.generate_treemap((x, y, w, height)))
                if size != 1:
                    x += w
                    tot_w += w
        elif height > width:
            tot_h = 0
            for subtree in self._subtrees:
                size = round(subtree.data_size / self.data_size, 2)
                h = round(height * size, 2)
                if subtree == self._subtrees[len(self._subtrees) - 1]:
                    tree.extend(subtree.generate_treemap((x, y, width,
                                                          height - tot_h)))
                else:
                    tree.extend(subtree.generate_treemap((x, y, width, h)))
                if size != 1:
                    y += h
                    tot_h += h
        else:
            tot_h = 0
            tot_w = 0
            for subtree in self._subtrees:
                size = round(subtree.data_size / self.data_size, 2)
                h = round(height * size, 2)
                w = round(width * size, 2)
                if subtree == self._subtrees[len(self._subtrees) - 1]:
                    tree.extend(subtree.generate_treemap((x, y, width - tot_w,
                                                          height - tot_h)))
                else:
                    tree.extend(subtree.generate_treemap((x, y, w, h)))
                if size != 1:
                    y += h
                    x += w
                    tot_h += h
                    tot_w += w
        return tree

    def get_separator(self: AbstractTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        """
        path = self._root
        p = self._parent_tree
        while p is not None:
            path = p._root + '/' + path
            p = p._parent_tree
        return path

    def get_leaves(self: AbstractTree) -> list:
        """
        gets the leaves of the given AbstractTree
        """
        leaves = []
        if not self._subtrees:
            return [self]
        for subtree in self._subtrees:
            leaves.extend(subtree.get_leaves())
        return leaves

    def update_size(self: AbstractTree, leaf: AbstractTree, key: int) -> None:
        """
        updates the size of the given leaf and the overall given AbstractTree
        """
        delta = self.data_size * 0.01
        if not self._subtrees:
            if self != leaf:
                return
            if key == 1:
                self.data_size += self.data_size * 0.01
                p = self._parent_tree
                while p is not None:
                    p.data_size += delta
                    p = p._parent_tree
            elif key == 0:
                self.data_size -= self.data_size * 0.01
                p = self._parent_tree
                while p is not None:
                    p.data_size -= delta
                    p = p._parent_tree
        for subtree in self._subtrees:
            subtree.update_size(leaf, key)

    def delete_tree(self: AbstractTree, leaf: AbstractTree) -> None:
        """
        deletes the given leaf from the given AbstractTree
        """
        if leaf in self._subtrees:
            p = self._parent_tree
            while p is not None:
                p.data_size -= self.data_size
                p = p._parent_tree
            self._subtrees.remove(leaf)
            return
        for subtree in self._subtrees:
            subtree.delete_tree(leaf)


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self: FileSystemTree, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        self.data_size = os.path.getsize(path)
        subtrees = []
        if os.path.isdir(path):
            for file in os.listdir(path):
                new = os.path.join(path, file)

                tree = FileSystemTree(new)
                subtrees.append(tree)
        AbstractTree.__init__(self, os.path.basename(path), subtrees,
                              self.data_size)

    def get_leaves(self: FileSystemTree) -> list:
        """
            gets the leaves of the given AbstractTree
        """
        return AbstractTree.get_leaves(self)

    def get_separator(self: FileSystemTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        """
        return AbstractTree.get_separator(self)

    def update_size(self: FileSystemTree, leaf: AbstractTree, key: int) -> None:
        """
        updates the size of the given leaf and the overall given AbstractTree
        """
        AbstractTree.update_size(self, leaf, key)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'extra-imports': ['os', 'random', 'math'],
            'generated-members': 'pygame.*'})
