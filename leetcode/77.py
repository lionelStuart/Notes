from tkinter import NO


class Solution:
    # 1到n范围内k个数的N种组合，选数不选数，做组合K，迭代，自顶向下
    def combine2(self, n: int, k: int):
        return self.traverse(1, n, k)
        
    
    def traverse(self, st, et, k):
        if et -st + 1 < k:
            return None
        if k == 1:
            ret = list()
            for i in range(st, et+1):
                ret.append([i])
            return ret
        
        c = self.traverse(st+1, et, k-1)

        lst = list()
        for i in c:
            i.append(st)
            lst.append(i)
        r = self.traverse(st+1, et, k)

        if r:
            for i in r:
                lst.append(i)
        return lst
    
    
    # 1到n范围内k个数的N种组合，选数不选数，做组合K，迭代，自底向上
    def combine(self, n: int, k: int):
        if n < k:
            return []
        
        tmp = [[1], []]
        for i in range(2, n+1):
            nw = list()
            for j in tmp:
                if len(j) == k:
                    continue
                cp = j.copy()
                cp.append(i)
                nw.append(cp)
            for p in nw:
                tmp.append(p)
            # print(tmp)
            # 剪枝
            idx = 0
            while idx < len(tmp):
                if n-i+len(tmp[idx]) <k:
                    # print('remove', tmp[idx], 'l=', len(tmp))
                    tmp.pop(idx)
                else:
                    idx +=1
                    
        print(len(tmp))
            
        ret = []
        for i in tmp:
            if len(i) == k:
                ret.append(i)
        return ret

if __name__ == '__main__':
    pass
    s = Solution()
    n = 4
    k = 2
    ret = s.combine(n, k)
    print(ret)