class Solution:
    # 三数和，返回不重复的组合,排序+双指针
    def threeSum(self, nums):
        if len(nums) < 3:
            return[[]]
        nums.sort()
        curr = 0
        ret = []
        print(nums)
        while curr != len(nums)-2:
            if curr > 0 and nums[curr] == nums[curr-1]:
                curr += 1
                continue
            tgt = - nums[curr]
            left = curr + 1
            right = len(nums) - 1
            tmp = list()
            while left < right:
                val = nums[left] + nums[right]
                if val == tgt:
                    tmp.append([nums[curr], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left+1]:
                        left += 1
                    while left < right and nums[right] == nums[right-1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif val > tgt:
                    right -= 1
                else:
                    left += 1
            for i in tmp:
                ret.append(i)
            curr += 1
        return ret
if __name__ == '__main__':
    s = Solution()
    nums = [-1,0,1,2,-1,-4]
    ret = s.threeSum(nums)
    print(ret)