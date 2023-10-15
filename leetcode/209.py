class Solution:
    # 长度最小子数组 滑窗法
    def minSubArrayLen(self, target: int, nums):
        lst = [0]
        cnt = 0
        for i in nums:
            cnt += i
            lst.append(cnt)
        
        left= 0
        right = 0
        while right < len(lst) and lst[right] < target:
            right += 1
        if right == len(lst):
            return 0
        
        ret = right - left
        while right < len(lst):
            while left < right and lst[right] - lst[left+1] >= target:
                left +=1
            ret = min(ret, right-left)
            right += 1
        return ret

        



if __name__ == '__main__':
    s = Solution()
    target = 11
    nums = [1,1,1,1,1,1,1,1]
    print(s.minSubArrayLen(target, nums))     