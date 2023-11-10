class Solution:
    def coinChange(self, coins, amount: int) -> int:
        if amount == 0:
            return 0
        dp = [amount+1 for i in range(amount+1)]
        for i in coins:
            if i < len(dp):
                dp[i] = 1
        
        for i in range(1, amount+1):
            for c in coins:
                if i + c <= amount:
                    dp[i+c] = min(dp[i+c], dp[i]+1)

        if dp[-1] == (amount+1):
            return -1
        return dp[-1]

        
        
        
if __name__ =='__main__':
    coins = [1, 2, 5]
    amount = 11
    
    coins = [2]
    amount = 3
    
    coins = [1]
    amount = 0
    
    so = Solution()
    ret = so.coinChange(coins, amount)
    print(ret)