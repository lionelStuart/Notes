class Solution:
    # 存在重复元素 哈希
    def containsNearbyDuplicate(self, nums, k: int) -> bool:
        pass
        m = dict()
        for idx in range(len(nums)):
            curr = nums[idx]
            if curr in m:
                if abs(m[curr]-idx) <=k:
                    return True
                else:
                    m[curr] = idx
            else:
                m[curr] = idx
        return False

if __name__ == '__main__':
    s = Solution()
    nums = [1,2,3,1]
    k = 3
    ret = s.containsNearbyDuplicate(nums, k)
    print(ret)