class Solution:
    # TOPN 堆排序
    def findKthLargest(self, nums, k: int) -> int:
         
        for i in range(k//2-1,-1,-1):
            self.heapify(nums, i, k)

        for i in range(k, len(nums)):
            if nums[i] > nums[0]:
                self.swap(nums, 0, i)
                self.heapify(nums, 0, k)

        return nums[0]        
    
    def heapify(self, num, k:int, n:int):
        left = k * 2 + 1
        right = k * 2 + 2
        small = k
        if left < n and num[left] < num[small]:
            small = left
        if right < n and num[right] < num[small]:
            small = right
        if small != k:
            self.swap(num, small, k)
            self.heapify(num, small, n)
            
    def swap(self, num, a, b):
        tmp = num[a]
        num[a] = num[b]
        num[b] = tmp 
    
if __name__ == '__main__':
    s = Solution()
    nums = [3,2,1,5,6,4] 
    k = 2
    ret = s.findKthLargest(nums, k)
    print(ret)