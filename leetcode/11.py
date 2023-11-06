class Solution:
    # 能接最多雨滴的容器，接雨滴的前置题，双指针移动最小边长
    def maxArea(self, height) -> int:
        st = 0
        et = len(height) -1 
        ret = -1
        while st < et:
            ret = max(ret, min(height[st], height[et]) * (et-st))
            if height[st] < height[et]:
                st += 1
            else:
                et -= 1
        return ret


if __name__ == '__main__':
    s = Solution()
    h = [1,8,6,2,5,4,8,3,7]
    ret = s.maxArea(h)
    print(ret)