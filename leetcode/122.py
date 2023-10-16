class Solution:
    # 买卖股票， 多次 DP， 峰值累加
    def maxProfit(self, prices) -> int:
        if len(prices) == 0:
            return 0
        tgt = 0 
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                tgt += prices[i]-prices[i-1]
        return tgt
        
if __name__ == '__main__':
    s = Solution()
    p = [7,1,5,3,6,4]
    ret = s.maxProfit(p)
    print(ret)