class Solution:
    def wordBreak(self, s: str, wordDict) -> bool:
        idx = 0
        dp = [0 for i in range(len(s))]

        while idx < len(s):
            if idx != 0 and dp[idx] != 1:
                idx += 1
                continue
            curr = s[idx:]

            for w in wordDict:
                if curr.startswith(w):
                    nx = idx + len(w)
                    if nx == len(s):
                        return True
                    dp[nx] = 1
            idx += 1
        return False
        
if __name__ =='__main__':
    s = "leetcode"
    wordDict = ["leet", "code"]
    so = Solution()
    ret = so.wordBreak(s,wordDict)
    print(ret)