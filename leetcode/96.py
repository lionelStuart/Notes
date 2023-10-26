class Solution:
    # 二叉搜索树的个数，节点M的二叉树个数等于f(M-1)*f(N-M+1),计算每个节点的二叉树数量和
    def numTrees(self, n: int) -> int:
        if n <= 1:
            return 1
        x = [0]*(n+1)
        x[0] = 1
        x[1] = 1
        for i in range(2, n+1):
            for j in range(0, i):
                x[i] += x[j]*x[i-j-1]
        # print(x)
        return x[-1]
if __name__ == '__main__':
    pass
    s = Solution()
    n = 3
    print(s.numTrees(n))