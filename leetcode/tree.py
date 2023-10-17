

from tkinter import NO


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
def build_tree(lst:list):
    if len(lst) == 0:
        return None
    
    nodes = list()
    for idx in range(len(lst)):
        if not lst[idx]:
            nodes.append(None)
            continue
        nodes.append(TreeNode(lst[idx]))
        if idx > 0 and idx %2 == 1:
            nodes[idx//2].left = nodes[-1]
        elif idx > 0:
            nodes[idx//2-1].right = nodes[-1]
    return nodes[0]

def print_tree(root):
    if not root:
        return
    lst = [root]
    while len(lst) > 0:
        tmp = []
        nq = []
        for i in lst:
            v = i.val if i else 'None'
            tmp.append(v)
            if i and i.left:
                nq.append(i.left)
            if i and i.right:
                nq.append(i.right)
        print(tmp)
        lst = nq
        
        
if __name__ == '__main__':
    root = [3,2,3,None,3,None,1]
    r = build_tree(root)
    print_tree(r)