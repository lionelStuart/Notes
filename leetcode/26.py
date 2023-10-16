# from turtle import right


class Solution:
    # 删除重复一次的元素
    def removeDuplicates(self, nums) -> int:
        pass
        
        if len(nums) < 2:
            return len(nums)
        left = 0
        right = 1
        while right < len(nums):
            while right < len(nums) and nums[right] <= nums[left]:
                right += 1
            if right < len(nums) and right - left > 1:
                self.swap(nums, left+1,right)
                left += 1
            elif right < len(nums):
                left += 1
        return left+1

        
        return 0
    
    def swap(self, nums, a, b):
        tmp = nums[a]
        nums[a] = nums[b]
        nums[b] = tmp
                
                

if __name__ == '__main__':

    s = Solution()
    nums = [0,0,1,1,1,2,2,3,3,4]
    ret = s.removeDuplicates(nums)
    print(ret, nums)