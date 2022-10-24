class Node:
    def __init__(self, elm, left=None, right=None):
        self.elm = elm
        self.left, self.right = left, right
def insert_bal(root,x):
    if root is None:
        return Node(x)
    else :
        root.left, root.right = insert_bal(root.right,x),root.left
        return root

def t_max(root):
    if root is None:
        return None
    else:
        left = t_max(root.left)
        right = t_max(root.right)
        if left and right is None:
            max = root.elm
            return max
        max = max(left,right)
        return max

if __name__ == "main":
    root = Node(elm = 0, left = None, right = None)
    insert_bal(root,1)
    insert_bal(root,2)
    insert_bal(root,3)
    insert_bal(root,4)
    insert_bal(root,5)
    max1 = t_max(root)
    print(max1)
