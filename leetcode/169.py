class Solution:
    # 多数元素，去票
    def majorityElement(self, nums) -> int:
        pass
        v = 0
        ret = 0
        for idx in range(len(nums)):
            if v == 0:
                ret = nums[idx]
                v += 1
                continue
            if nums[idx] == ret:
                v += 1
            else:
                v -= 1
        return ret
            
if __name__ == '__main__':
    s = Solution()
    nums = [2,2,1,1,1,2,2]
    ret = s.majorityElement(nums)
    print(ret)