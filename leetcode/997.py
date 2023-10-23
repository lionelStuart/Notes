class Solution:
    # 图问题
    # 找到小镇法官，找到无信任的候选，存在于所有被信任的集合中
    def findJudge(self, n: int, trust) -> int:
        m = dict()
        for i in trust:
            if i[0] in m:
                m[i[0]].add(i[1])
            else:
                m[i[0]] = {i[1]}
        cad = list()
        for i in range(1, n+1):
            if i not in m:
                cad.append(i)
        # print(cad)
        
        for c in cad:
            tag = True
            for i in range(1, n+1):
                if i == c:
                    continue
                if i not in m or c not in m[i]:
                    tag = False
                    break
            if tag is True:
                return c
        return -1
        
        
if __name__ == '__main__':
    s = Solution()
    n = 2 
    trust = []
    ret = s.findJudge(n, trust)
    print(ret)