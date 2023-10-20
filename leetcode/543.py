from tree import *

class Solution:
    def diameterOfBinaryTree(self, root) -> int:
        self.dem = 0
        self.dfs(root)
        return self.dem
        
    def dfs(self,root):
        if not root.left and not root.right:
            return 0
        dpl = 0
        dpr = 0
        if root.left:
            dpl = self.dfs(root.left) + 1
        if root.right:
            dpr = self.dfs(root.right) + 1
        self.dem = max(self.dem, dpl + dpr)
        return max(dpl, dpr)
        
if __name__ == '__main__':
    s = Solution()
    head = [1,2]
    root = build_tree(head)
    ret = s.diameterOfBinaryTree(root)
    print(ret)