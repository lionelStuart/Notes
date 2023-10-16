class Solution:
    # 合并有序数组 双指针
    def merge(self, nums1, m: int, nums2, n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        left = m-1
        right = n-1
        tgt = m+n-1
        while tgt != -1:
            if left != -1 and right != -1 and nums1[left] > nums2[right]:
                nums1[tgt] = nums1[left]
                left -= 1
            elif left != -1 and right != -1:
                nums1[tgt] = nums2[right]
                right -= 1
            elif left != -1:
                nums1[tgt] = nums1[left]
                left -= 1
            else:
                nums1[tgt] = nums2[right]
                right -= 1
            tgt -= 1
        
                
                
                

if __name__ == '__main__':

    s = Solution()
    nums1 = [1,2,3,0,0,0]
    m = 3
    nums2 = [2,5,6]
    n = 3
    ret = s.merge(nums1, m, nums2, n)
    print(nums1)