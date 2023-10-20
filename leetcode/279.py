class Solution:
    # 计算N的最小平方数和，用计算最少零钱的方案，平方数为1，自底向上拼凑最小数
    def numSquares(self, n: int) -> int:
        lst = [i for i in range(n+1)]
        c = 1
        cad = list()
        while c*c<n+1:
            lst[c*c] = 1
            cad.append(c*c)
            c += 1
        for i in range(1,n+1):
            for j in cad:
                if j + i > n:
                    break
                lst[i+j] = min(lst[i]+1, lst[i+j])
        return lst[-1]
        
if __name__ == '__main__':
    s = Solution()
    head = 13
    ret = s.numSquares(head)
    print(ret)