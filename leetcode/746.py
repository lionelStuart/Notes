class Solution:
    def minCostClimbingStairs(self, cost) -> int:
        if len(cost) == 0:
            return 0
        elif len(cost) == 1:
            return cost[1]
        f0 = cost[0]
        f1 = cost[1]
        for i in range(2, len(cost)):
            curr = min(f0, f1) + cost[i]
            f0 = f1
            f1 = curr
        return min(f0, f1)

if __name__ == '__main__':
    s = Solution()
    cost = [1,100,1,1,1,100,1,1,100,1]
    ret = s.minCostClimbingStairs(cost)
    print(ret)
    pass