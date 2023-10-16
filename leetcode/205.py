class Solution:
    # 同构字符串，哈希表记录字符首次索引位置
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        ms = dict()
        mt = dict()
        for i in range(len(s)):
            if s[i] not in ms:
                ms[s[i]] = i
            if t[i] not in mt:
                mt[t[i]] = i
            if ms[s[i]] != mt[t[i]]:
                return False
        return True
            
if __name__ == '__main__':
    s = Solution()
    ss = "egg"
    tt = "add"
    
    ret = s.isIsomorphic(ss, tt)
    print(ret)