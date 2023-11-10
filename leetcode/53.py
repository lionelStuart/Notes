class Solution:
    def maxSubArray(self, nums):
        sm = [nums[0]]
        for i in range(1, len(nums)):
            sm.append(sm[-1]+nums[i])
        ret = sm[0]
        mi = 0
        print(sm)
        for i in range(0, len(nums)):
            # ret = max(ret, sm[i]-mi, nums[i])
            ret = max(ret, sm[i]-mi)
            if sm[i] < mi:
                mi = sm[i]
        return ret
  

# class Solution:
#     def maxSubArray(self, nums: List[int]) -> int:
#         return max_add_seq(nums)
# def max_add_seq(nums):
#     dp = list()
#     dp.append(nums[0])
#     for i, v in enumerate(nums):
#         if i == 0:
#             continue
#         dp.append(max(dp[i - 1] + nums[i], nums[i]))
#     m = nums[0]
#     for v in dp:
#         # print(v)
#         if v > m:
#             m = v
#     return m

if __name__ == '__main__':
    s = Solution()
    nums = [-1,1,2,1]
    val = s.maxSubArray(nums)
    print(val)