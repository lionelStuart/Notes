class Solution:
    # 数每层平均数 BFS
    def averageOfLevels(self, root):
        if root is None:
            return []
        q = [root]
        ret = list()
        while len(q):
            cnt = 0
            nq = list()
            for i in q:
                cnt += i.val
                if i.left:
                    nq.append(i.left)
                if i.right:
                    nq.append(i.right)
            ret.append(cnt / len(q))
            q = nq
        return ret
        

    if __name__ == '__main__':
        pass
        s = Solution()
        s.averageOfLevels()