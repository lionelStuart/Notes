# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

from leetcode.tree import *

class Solution:
    # 查找最紧公共祖先，可以按链表查，也可以如下：如果从左支和右支都能找到节点，则取父节点，否则取能找到的节点，即最先遇到的节点
    def lowestCommonAncestor(self, root, p, q):
        if root is None:
            return None
        if root.val == p.val or root.val == q.val:
            return root
        
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left is not None and right is not None:
            return root
        if not left:
            return left
        return right
            
    
            
        
        