import re


class Solution:
    # 不用除法求每个位置的积，双向累乘
    def productExceptSelf(self, nums):
        if len(nums) < 1:
            return 
        left = [1]
        right = [1]
        for i in range(0, len(nums)-1):
            left.append(left[-1]*nums[i])
            right.append(right[-1]*nums[len(nums)-i-1])
        right.reverse()
        ret = list()
        for i in range(len(nums)):
            ret.append(left[i]*right[i])
        return ret
                        
if __name__ == '__main__':
    pass
    s = Solution()
    nums = [1,2,3,4]
    print(s.productExceptSelf(nums))