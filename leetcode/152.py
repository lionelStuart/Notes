class Solution:
    # 求最大连续乘积和，DP，正负数会导致最大，最小值翻转，需要记录以idx【包含idx位置】结尾数组的最大和最小值，
    # 则最大，最小值数组仅与前一个数相关，最后求max数组中的最大值
    def maxProduct(self, nums) -> int:
        if len(nums) == 0:
            return -1
        mx = [nums[i] for i in range(len(nums))]
        mi = [nums[i] for i in range(len(nums))]
        for idx in range(1, len(nums)):
            mx[idx] = max(mx[idx], mx[idx-1]*nums[idx])
            mx[idx] = max(mx[idx], mi[idx-1]*nums[idx])
            
            mi[idx] = min(mi[idx], mx[idx-1]*nums[idx])
            mi[idx] = min(mi[idx], mi[idx-1]*nums[idx])
        return max(mx)        
if __name__ == '__main__':
    s = Solution()
    nums = [-2,0,-1]
    ret = s.maxProduct(nums)
    print(ret)