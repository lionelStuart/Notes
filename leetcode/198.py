class Solution:
    def rob(self, nums):
        f0 = [0 for i in range(len(nums))]
        f1 = [0 for i in range(len(nums))]
        f1[0] = nums[0]
        for idx in range(1, len(nums)):
            f0[idx] = max(f1[idx-1],f0[idx-1])
            f1[idx] = f0[idx-1] + nums[idx]
        return max(f1[-1], f0[-1])
    
                
if __name__ == '__main__':
    s = Solution()
    nums = [2,7,9,3,1]
    ret = s.rob(nums)
    print(ret)