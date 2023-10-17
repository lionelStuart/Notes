class Solution:
    # 跳跃游戏，最少跳数, 动态规划，求到当前位置的最少跳数，当跳跃位置超过末尾时加入结果集合
    def jump(self, nums) -> int:
        pass
        if len(nums) <= 1:
            return 0
        f = [len(nums) for i in range(len(nums))]
        f[0] = 0
        ret = []
        for i in range(0, len(nums)):
            for j in range(i+1, nums[i]+i+1):
                if j>= len(nums)-1:
                    ret.append(f[i]+1)
                    # 贪心，从首次到达的位置是最少跳数
                    # return f[i] + 1
                    break
                f[j] = min(f[j], f[i]+1)
        #         print(j, f[j], ret, f)
        #     print('lllooop')
        # print(f)
        return min(ret)
          
if __name__ == '__main__':
    pass
    s = Solution()
    nums = [2,3,0,1,4]
    print(s.jump(nums))