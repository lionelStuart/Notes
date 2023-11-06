class Solution:
    # 字母异位词分组，统计字符频率作为key进行分组
    def groupAnagrams(self, strs):
        m = dict()
        for word in strs:
            cnt = dict()
            for i in word:
                if i not in cnt:
                    cnt[i] = 1
                else:
                    cnt[i] += 1
            key = ''
            tmp = sorted(cnt.keys())
            for i in tmp:
                key += f'{i}{cnt[i]}'
            if key not in m:
                m[key] = [word]
            else:
                m[key].append(word)
        ret = []
        for i in m:
            # print(m[i])
            ret.append(m[i])
        return ret
        
if __name__ =='__main__':
    s = Solution()
    v = strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    ret = s.groupAnagrams(v)
    print(ret)