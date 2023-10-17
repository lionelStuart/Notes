class Solution:
    # 跳跃游戏，最后一个位置是否可达 动态规划，求解最远位置区间是否可达最后一个位置
    def canJump(self, nums) -> bool:
        if len(nums) == 0:
            return False
        left = 0
        right = nums[left]
        mx = right
        while right <len(nums) and left < right:
            for i in range(left, right+1):
                mx = max(nums[i]+i, mx)
            if mx >= len(nums)-1:
                return True
            if mx <= right:
                return False
            left = right
            right = mx
        return right >= len(nums)-1
                        
if __name__ == '__main__':
    pass
    s = Solution()
    nums = [0]
    print(s.canJump(nums))