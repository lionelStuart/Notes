from sympy import trace

from leetcode.tree import build_tree


class Solution:
    # 返回树的右视图，从右侧遍历树的所有分支，截断超长的部分
    def rightSideView(self, root):
        self.traces = list()
        tmp = list()
        ret = []
        self.dfs(root, tmp)
        for i in self.traces:
            mx = len(ret)
            if len(i) <= mx:
                continue
            for j in range(mx, len(i)):
                ret.append(i[j]) 
        return ret

    def dfs(self, root, lst):
        if not root:
            self.traces.append(lst)
            return []
        lst.append(root.val)
            
        self.dfs(root.right, lst.copy())
        self.dfs(root.left, lst.copy())
        
if __name__ == '__main__':
    s = Solution()
    head = []
    root = build_tree(head)
    ret = s.rightSideView(root)
    print(ret)