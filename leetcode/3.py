class Solution:
    # 无重复字符最长字串 滑窗双指针
    def lengthOfLongestSubstring(self, s: str):
        left = 0
        right = 0
        m = dict()
        ret = 0
        while right < len(s):
            ch = s[right]
            if ch not in m or m[ch] == -1:
                m[ch] = right

            else:
                left = m[ch] + 1
                for k in m:
                    if m[k] < left:
                        m[k] = -1
                m[ch] = right
            ret = max(ret, right - left + 1)
            right += 1
                
        return ret
    
    
if __name__ == '__main__':

    s = Solution()
    ss = "abba"
    ret = s.lengthOfLongestSubstring(ss)
    print(ret)