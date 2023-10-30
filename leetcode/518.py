class Solution:
    def change2(self, amount: int, coins):
        if len(coins) == 0:
            return 0
        # if amount == 0:
        #     return 1
        ret = 0
        cnt = 0
        while cnt*coins[0]<=amount:
            curr = cnt*coins[0]
            if amount-curr == 0:
                ret += 1
                break
            tmp = self.change2(amount-curr, coins[1:])
            ret += tmp
            cnt += 1
        print('get amout=', amount, ' count=', ret)
        return ret

    def change(self, amount: int, coins):
        # 硬币能凑出的方案数量
        # 需要顺序拆解的数目，
        # 每次只选一种硬币，能到达的位置为当前位置+硬币的值，即选定硬币后当前位置的方案数累加到下一个位置上
        # 按指定硬币指定步长将范围内的集合选满，获得到达amount的方案数量
        lst = [0]*(amount+1)    
        lst[0] = 1
        for j in coins:
            for i in range(amount+1):
                if j + i <= amount:
                    lst[j+i] += lst[i]
        return lst[-1]

if __name__ == '__main__':
    amount = 5
    coins = [1, 2, 5]
    
    amount = 3
    coins = [2]
    
    amount = 10
    coins = [10] 
    s = Solution()
    ret = s.change(amount, coins)
    print(ret)
    pass
