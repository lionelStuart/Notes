from leetcode.tree import *
from leetcode.tree import build_tree

class Solution:
    # 打家劫舍III, 在二叉树上实现
    def rob(self, root) -> int:
       if not root:
           return 0
       self.m0 = dict()
       self.m1 = dict()
       self.dfs(root)
       return max(self.m0[root], self.m1[root])
    
    def dfs(self, root):
        if not root:
            return
        if root.left:
            self.dfs(root.left)
        if root.right:
            self.dfs(root.right)
        
        lf0 = self.m0[root.left] if root.left else 0
        lf1 = self.m1[root.left] if root.left else 0
        rf0 = self.m0[root.right] if root.right else 0
        rf1 = self.m1[root.right] if root.right else 0

        self.m0[root] = max(lf0, lf1) + max(rf0, rf1)
        self.m1[root] = lf0 + rf0 + root.val
        
             
         
        
if __name__ == '__main__':
    pass
    s = Solution()
    root = [3,2,3,None,3,None,1]
    root = [3,4,5,1,3,None,1]
    r= build_tree(root)
    print(s.rob(r))