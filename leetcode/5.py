from more_itertools import random_combination_with_replacement
from sympy import jacobi


# class Solution:
#     # DP解法求最长回文子串(连续),
#     # 和不连续回文子序列的解题思路一样， 对 序列a, cac = 1+2 , cab = max(ca) = a，字串i+1,j+1能够变长的条件为i，j为回文串，则二维矩阵记录当前串是否为回文串，斜行向上迭代
#     # 斜行循环方式为
#     # for i in range(n):
#     #   x = 0
#     #   y = i
#     #   for j in range(n-i):
#     #        mat[x+j][y+j] ... 
#     def longestPalindrome(self, s: str) -> str:
#         n = len(s)
#         mat = [[True]*n for i in range(n)]
        
#         mx = 1
#         curr = s[0]
        
#         for j in range(n):
#             x = 0
#             y = j
#             for i in range(n-j):
#                 if x == y:
#                     mat[x+i][y+i] = True
#                     continue
#                 if s[x+i] == s[y+i]:
#                     mat[x+i][y+i] = mat[x+i+1][y+i-1]
#                 else:
#                     mat[x+i][y+i] = False
#                 if mat[x+i][y+i] and y-x+1 > mx:
#                         curr = s[x+i:y+i+1]
#                         mx = y-x+1
#             # for i in mat:
#             #     print(i)
            
#         return curr


class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        mat = [[True]*n for i in range(n)]

        mx = 1
        mx_str = s[0]

        for i in range(1, n):
            x = 0
            y = i
            for j in range(0, n-i):
                if s[x+j] == s[y+j]:
                    mat[x+j][y+j] = mat[x+j+1][y+j-1]
                else:
                    mat[x+j][y+j] = False
                if mat[x+j][y+j] and y-x + 1 > mx:
                        mx = y-x+1
                        mx_str = s[x+j:y+j+1]
                        print(mx_str)
        return mx_str
if __name__ == '__main__':
    s = Solution()
    sss = "babad"
    sss = "cbbd"
    # sss = 'bb'
    v = s.longestPalindrome(sss)    
    print(v)