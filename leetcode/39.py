class Solution:
    def combinationSum(self, candidates, target):
        self.ret = list()
        tmp = list()
        for i in candidates:
            if i == target:
                self.ret.append([i])
                candidates.remove(i)
        # print('cad=', candidates)
        self.dfs(candidates, tmp, target)
        return self.ret
        
    def dfs(self, candidates, tmp, target):
        if len(candidates) == 0 and target == 0:
            self.ret.append(tmp)
        if len(candidates) == 0:
            return
        for i in candidates:
            if i == target:
                t = tmp.copy()
                t.append(i)
                self.ret.append(t)
        curr = candidates[0]
        cnt = 0
        sum = 0
        while sum <= target:
            t = tmp.copy()
            for i in range(cnt):
                t.append(curr)
            self.dfs(candidates[1:], t, target-sum)
            sum +=curr
            cnt += 1
                    
        
if __name__ == '__main__':
    s = Solution()
    candidates = [2,3,5]
    target = 8
    ret = s.combinationSum(candidates, target)
    print(ret)