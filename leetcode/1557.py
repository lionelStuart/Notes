class Solution:
    # 可以到达所有点数的最少点数，DAG图，头节点无法被访问到，等价于找到所有头节点
    def findSmallestSetOfVertices(self, n: int, edges):
        l = [1 for i in range(n)]
        for i in edges:
            to = i[1]
            l[to] = 0
        ret = list()
        for idx in range(n):
            if l[idx] == 1:
                ret.append(idx)
        return ret
        
        
if __name__ == '__main__':
    s = Solution()
    n = 6
    edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
    ret = s.findSmallestSetOfVertices(n, edges)
    print(ret)        