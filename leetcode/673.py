class Solution:
    def findNumberOfLIS(self, nums) -> int:
        # 最长递增子序列的个数
        # 在最长递增子序列的基础上记录增长个数
        # 如果个数发生递增，该位置上的子序列树为增长子序列个数的和
        seq = [1]*len(nums)
        cnt = [0]*len(nums)
        
        for i in range(len(nums)):
            for j in range(i):
                if nums[j]<nums[i]:      
                    seq[i] = max(seq[i],seq[j]+1)
            if seq[i] == 1:
                cnt[i] = 1
                continue
            c = 0
            for j in range(i):
                if nums[j]<nums[i] and seq[j] == seq[i]-1:
                    c += cnt[j]
            cnt[i] = c

        mx = max(seq)
        ret = 0
        for i in range(len(nums)):
            if seq[i] == mx:
                ret += cnt[i]
        # print(seq)
        # print(cnt)
        return ret
        
if __name__ == '__main__':
    pass
    s = Solution()
    l = [1,3,5,4,7]
    ret = s.findNumberOfLIS(l)
    print(ret)