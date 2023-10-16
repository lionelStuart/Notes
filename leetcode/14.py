from email import header


class Solution:
    # 字符串数组最长公共前缀
    def longestCommonPrefix(self, strs) -> str:
        if len(strs) == 0:
            return ""
        n = len(strs[0])
        for i in strs:
            n = min(len(i), n)
        
        idx = 0
        tgt = ""
        while idx < n:
            curr = strs[0][idx]
            for i in strs:
                if i[idx] != curr:
                    return tgt
            idx += 1
            tgt +=curr
        return tgt 
    
if __name__ == '__main__':
    s = Solution()
    strs = ["flower","flow","flight"]
    ret = s.longestCommonPrefix(strs)
    print(ret)