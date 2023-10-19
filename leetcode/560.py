import re


class Solution:
    # 前缀树，获取已累加的和
    def subarraySum(self, nums, k: int) -> int:
        if len(nums) == 0:
            return 0
        sum = [v for v in nums]
        cnt = 0

        for idx in range(0, len(nums)):
            if sum[idx] == k:
                cnt += 1

            for i in range(idx):
                sum[i] += nums[idx]
                if sum[i] == k:
                    cnt += 1

        return cnt
        
if __name__ == '__main__':
    s = Solution()
    n = [1,2,3]
    k = 3
    ret = s.subarraySum(n, k)
    print(ret)