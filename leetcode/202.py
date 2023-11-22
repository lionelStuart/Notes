import math
class Solution:
    def isHappy(self, n: int) -> bool:
        tgt = n
        while tgt*tgt >= 10:
            sm = 0
            while tgt > 0:
                sm +=(tgt % 10) * (tgt % 10)
                tgt = tgt // 10 
            tgt = sm
            print(tgt)
        return int(tgt) == 1
    
if __name__ == '__main__':
    s = Solution()
    ret = s.isHappy(4)
    print(ret)