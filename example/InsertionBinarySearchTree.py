class Node:
    def __init__(self, key, value):
        self.key, self.value = key, value
        self.left = self.right = None
def insert(root, key, value):
    if root is None:
        return Node(key, value)
    else:
        if key == root.key:
            root.value = value
        elif key < root.key:
            root.left = insert(root.left, key, value)
        else:
            root.right = insert(root.right, key, value)
        return root
