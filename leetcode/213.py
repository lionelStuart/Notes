class Solution:
    # 打家劫舍1， 不可相邻,且是环形队列,拆解子问题，分解初始状态
    def rob(self, nums):
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]
        return max(self.rob0(nums[1:]), self.rob0(nums[:-1]))
    
    def rob0(self, nums):
        f0 = [0 for i in range(len(nums))]
        f1 = [0 for i in range(len(nums))]
        f1[0] = nums[0]
        for idx in range(1, len(nums)):
            f0[idx] = max(f1[idx-1],f0[idx-1])
            f1[idx] = f0[idx-1] + nums[idx]
        return max(f1[-1], f0[-1])