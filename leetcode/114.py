from leetcode.tree import build_tree, print_tree

class Solution:
    # 把二叉树前序展开为列表，左节点为空，保存在右节点上
    def flatten(self, root) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        self.dfs(root)
        curr = root
        while curr:
            print(curr.val)
            curr = curr.right
    
    
    def dfs(self, root):
        if root is None:
            return None, None
        if root.left is None and root.right is None:
            return root, root
        
        head = root
        tail = root
        right = root.right        
        if root.left:
            h, t = self.dfs(root.left)
            head.right = h
            tail = t
        if right:
            h, t = self.dfs(right)
            tail.right = h
            tail = t
        root.left = None
        return head, tail
        
if __name__ == '__main__':
    s = Solution()
    head = [1,2,5,3,4,None,6]
    root = build_tree(head)
    # print_tree(root)
    s.flatten(root)