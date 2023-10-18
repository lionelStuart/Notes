class Solution:
    # 删除有序数组重复项，超过两次，冒泡法
    def removeDuplicates2(self, nums) -> int:
        pass
        if len(nums) < 3:
            return len(nums)
        
        left = 1
        mx = len(nums)
        while left < mx:
            if nums[left] > nums[left-1]:
                left += 1
                continue
            if left+1 < mx and nums[left+1] == nums[left]:
                right = left + 1
                while right < mx and nums[right] == nums[left]:
                    right += 1
                st = left + 1
                while right < mx:
                    nums[st] = nums[right]
                    st += 1
                    right += 1
                mx = st
            left +=1
        return mx
    
    
    # 删除有序数组重复项，超过两次，快慢指针,为当前位置赋值，值从快指针获取
    def removeDuplicates(self, nums) -> int:
        if len(nums) < 3:
            return len(nums)
        
        left = 2
        right = 2
        while right < len(nums):
            if nums[right] != nums[left-2]:
                nums[left] = nums[right]
                left += 1
            right += 1
        print(nums)
        return left
        
        
    def swap(self, nums,a, b):
        tmp = nums[a]
        nums[a] = nums[b]
        nums[b] = tmp
        
          
if __name__ == '__main__':
    pass
    s = Solution()
    nums = [1,1,1,2,2,3]
    print(s.removeDuplicates(nums))