from email import header


class Solution:
    # 双指针，接雨水，两边柱子取最短板
    def trap(self, height) -> int:
        if len(height) < 2:
            return 0
        left = 0
        right = len(height) - 1
        mx_left = 0
        mx_right = 0
        ret = 0
        while left < right:
            mx_left = max(height[left], mx_left)
            mx_right = max(height[right], mx_right)
            if mx_right > mx_left:
                ret += mx_left - height[left]
                left += 1
            else:
                ret += mx_right - height[right]
                right -= 1
        return ret
    
if __name__ == '__main__':
    s = Solution()
    height = [4,2,0,3,2,5]
    ret = s.trap(height)
    print(ret)