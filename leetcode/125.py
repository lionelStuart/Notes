from curses.ascii import isalpha
from turtle import right


class Solution:
    # 验证回文串，双指针
    def isPalindrome(self, s: str) -> bool:        
        left = 0
        right = len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if left < right and s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
        
if __name__ == '__main__':
    s = Solution()
    ss = "0P"
    ret = s.isPalindrome(ss)
    print(ret)