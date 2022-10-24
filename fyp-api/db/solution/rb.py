from random import shuffle
from inorder import (
    inorder_nodes,
    reverse_inorder_nodes,
    AssocArray_KeysView,
    AssocArray_ValuesView,
    AssocArray_ItemsView)
from bst_assoc_array import find_node_i
from counter import global_counter


class Node:
    def __init__(self, key, value):
        self.key, self.value = key, value
        self.red = True
        self.left = self.right = None


def rotate_lr(q):
    global_counter.increase()
    p = q.left
    q.left = p.right
    p.right = q
    return p


def rotate_rl(q):
    global_counter.increase()
    p = q.right
    q.right = p.left
    p.left = q
    return p


def dist_black(root):
    root.red = True
    root.left.red = root.right.red = False


def left_larger(root):
    if root.left.red:
        if root.right and root.right.red:
            dist_black(root)
        elif root.left.left and root.left.left.red:
            root = rotate_lr(root)
            dist_black(root)
        elif root.left.right and root.left.right.red:
            root.left = rotate_rl(root.left)
            root = rotate_lr(root)
            dist_black(root)
    return root


def right_larger(root):
    if root.right.red:
        if root.left and root.left.red:
            dist_black(root)
        elif root.right.right and root.right.right.red:
            root = rotate_rl(root)
            dist_black(root)
        elif root.right.left and root.right.left.red:
            root.right = rotate_lr(root.right)
            root = rotate_rl(root)
            dist_black(root)
    return root


def insert(root, key, value):
    if root is None:
        return Node(key, value)
    else:
        if key == root.key:
            root.value = value
            return root
        elif key < root.key:
            root.left = insert(root.left, key, value)
            return left_larger(root)
        else:
            root.right = insert(root.right, key, value)
            return right_larger(root)


def turn_black(root):
    if root and root.red:
        root.red = False
        return True
    else:
        return False


def right_smaller(root, short, deleted):
    if short and not turn_black(root.right):
        red, lred = root.red, root.left.red
        root = rotate_lr(root)
        root.right.red = True
        root.red = False
        if lred:
            root.right = right_larger(rotate_lr(root.right))
            return (root, False, deleted)
        else:
            return (right_larger(root), not red, deleted)
    else:
        return (root, False, deleted)


def left_smaller(root, short, deleted):
    if short and not turn_black(root.left):
        red, rred = root.red, root.right.red
        root = rotate_rl(root)
        root.left.red = True
        root.red = False
        if rred:
            root.left = left_larger(rotate_rl(root.left))
            return (root, False, deleted)
        else:
            return (left_larger(root), not red, deleted)
    else:
        return (root, False, deleted)


def sub_root(sub, root):
    if turn_black(sub):
        return (sub, False, root)
    else:
        return (sub, not root.red, root)


def delete_rightmost(root):
    if root.right is None:
        return sub_root(root.left, root)
    else:
        root.right, short, rightmost = delete_rightmost(root.right)
        return right_smaller(root, short, rightmost)


def delete(root, key):
    if root is None:
        return (None, False, None)
    elif key == root.key:
        if root.left is None:
            return sub_root(root.right, root)
        elif root.right is None:
            return sub_root(root.left, root)
        else:
            sub, short, rightmost = delete_rightmost(root.left)
            rightmost.left, rightmost.right = sub, root.right
            rightmost.red = root.red
            return left_smaller(rightmost, short, root)
    elif key < root.key:
        root.left, short, deleted = delete(root.left, key)
        return left_smaller(root, short, deleted)
    else:
        root.right, short, deleted = delete(root.right, key)
        return right_smaller(root, short, deleted)


def is_rb_subs(left, right, red):
    l, lbh = is_rb_color(left, red)
    if l:
        r, rbh = is_rb_color(right, red)
        if r:
            if lbh == rbh:
                return (True, (0 if red else 1) + lbh)
            else:
                return (False, -2)
        else:
            return (False, rbh)
    else:
        return (False, lbh)


def is_rb_color(root, red):
    if root is None:
        return (True, 0)
    elif root.red and red:
        return (False, -1)
    else:
        return is_rb_subs(root.left, root.right, root.red)


def is_rb(root):
    if root is None:
        return (True, 0)
    else:
        return is_rb_subs(root.left, root.right, False)


class RBAssocArray:
    def __init__(self, s=None):
        global_counter.reset()
        self.root = None
        if s:
            for key, value in s:
                self[key] = value

    def __getitem__(self, key):
        p = find_node_i(self.root, key)
        if p is None:
            raise KeyError(key)
        return p.value

    def __contains__(self, key):
        return find_i(self.root, key) is not None

    def __setitem__(self, key, value):
        self.root = insert(self.root, key, value)

    def __delitem__(self, key):
        self.root, _, deleted = delete(self.root, key)
        if deleted is None:
            raise KeyError(key)

    def __iter__(self):
        yield from (p.key for p in inorder_nodes(self.root))

    def __reversed__(self):
        yield from (p.key for p in reverse_inorder_nodes(self.root))

    def keys(self):
        return AssocArray_KeysView(self)

    def values(self):
        return AssocArray_ValuesView(self)

    def items(self):
        return AssocArray_ItemsView(self)


if __name__ == '__main__':
    N = 10000
    m = RBAssocArray(zip(range(N), range(N)))
    print(is_rb(m.root))
    print(global_counter.get())

    s = list(range(N))
    shuffle(s)

    for i in range(N // 2):
        del m[s[i]]

    print(is_rb(m.root))

    s = list(range(N))
    shuffle(s)

    m = RBAssocArray()
    for x in s:
        m[x] = x

    print(is_rb(m.root))

    for x in s[:N - 20]:
        del m[x]

    for i in m.keys():
        print(i, m[i])
