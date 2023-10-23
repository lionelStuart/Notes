from leetcode.tree import *

class Solution:
    # 判断合法的二叉搜索树，需要位于树左右侧节点都符合大于小于规则
    # 等价于执行快排的反向操作，获取左右侧节点的最值与当前值比较
    def isValidBST(self, root) -> bool:
        if root is None:
            return False
        _, _, t = self.dfs(root)
        return t
    
    
    def dfs(self, root):
        if not root.left and not root.right:
            return root.val, root.val, True
        
        mi = root.val
        mx = root.val
        if root.left:
            a, b, t = self.dfs(root.left)
            mi = min(mi, a)
            mx = max(mx, b)
            if not t:
                return mi, mx, t
            if b >= root.val:
                return mi, mx, False
        
        if root.right:
            a, b, t = self.dfs(root.right)
            mi = min(mi, a)
            mx = max(mx, b)
            if not t:
                return mi, mx, t
            if a <= root.val:
                return mi, mx, False
        return mi, mx, True
        
    
if __name__ == '__main__':
    pass
    s = Solution()
    root = [2,1,3]
    t = build_tree(root)
    print(s.isValidBST(t))