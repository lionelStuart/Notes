from re import X


class Solution:
    # DP解法求解最长回文子序列(不连续)
    # 对序列a, bab = 1+2 caa = max(cb, aa)
    # 由于不连续，字串i+1,j+1相对i，j能够持续边长
    # 增长的条件为val(i)==val(j)
    # 增长则 f(i,j) = f(i-1,j-1) + 2，否则为max(f(i-1,j), f(i, j-1))
    # 在矩阵中只与左，下，左下的值相关
    # 斜向上求解
    # 求解所有的回文串，建立辅助的val矩阵，当长度变化时，取递增回文串，否则是max串或右下方的旧串
    
    def longestPalindromeSubseq(self, s: str) -> int:
        pass
        n = len(s)
        mat = [[0]*n for i in range(n)]
        
        val = [['']*n for i in range(n)]
        mx = 1
        value = set()
        for i in range(n):
            x = 0
            y = i
            for j in range(n-i):
                now = [x+j, y+j]
                if now[0] == now[1]:
                    mat[now[0]][now[1]] = 1
                    val[now[0]][now[1]] = s[now[0]]
                    value.add(s[now[0]])
                    continue
                if s[now[0]] == s[now[1]]:
                    mat[now[0]][now[1]] = mat[now[0]+1][now[1]-1] + 2
                    val[now[0]][now[1]] = f'{s[now[0]]}{val[now[0]+1][now[1]-1]}{s[now[0]]}'
                    value.add(val[now[0]][now[1]])
                else:
                    mat[now[0]][now[1]] = max(mat[now[0]][now[1]-1],mat[now[0]+1][now[1]])
                    if mat[0][now[1]-1] > mat[now[0]+1][now[1]]:
                        val[now[0]][now[1]] = val[now[0]][now[1]-1]
                    else:
                        val[now[0]][now[1]] = val[now[0]+1][now[1]]
                    # val[now[0]][now[1]] = f'{s[now[0]]}{val[now[0]+1][now[1]-1]}{s[now[0]]}'
                if mat[now[0]][now[1]] > mx:
                    mx = mat[now[0]][now[1]]
                    
        for i in val:
            print(i)
        print(value)
        return mx



if __name__ == '__main__':
    s = Solution()
    sss = "bbbab"
    # sss = "euazbipzncptldueeuechubrcourfpftcebikrxhybkymimgvldiwqvkszfycvqyvtiwfckexmowcxztkfyzqovbtmzpxojfofbvwnncajvrvdbvjhcrameamcfmcoxryjukhpljwszknhiypvyskmsujkuggpztltpgoczafmfelahqwjbhxtjmebnymdyxoeodqmvkxittxjnlltmoobsgzdfhismogqfpfhvqnxeuosjqqalvwhsidgiavcatjjgeztrjuoixxxoznklcxolgpuktirmduxdywwlbikaqkqajzbsjvdgjcnbtfksqhquiwnwflkldgdrqrnwmshdpykicozfowmumzeuznolmgjlltypyufpzjpuvucmesnnrwppheizkapovoloneaxpfinaontwtdqsdvzmqlgkdxlbeguackbdkftzbnynmcejtwudocemcfnuzbttcoew"
    v = s.longestPalindromeSubseq(sss)    
    print(v)