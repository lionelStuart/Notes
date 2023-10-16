from curses.ascii import isalpha
from turtle import right


class Solution:
    # 两数和唯一下标, 双指针
    def twoSum(self, numbers, target: int):
        pass
        left = 0
        right = len(numbers)-1
        while left < right:
            curr = numbers[left] + numbers[right]
            if curr == target:
                return [left+1, right+1]
            elif curr < target:
                left += 1
            else:
                right -= 1
        return []
    
        
if __name__ == '__main__':
    s = Solution()
    numbers = [2,7,11,15]
    target = 9
    ret = s.twoSum(numbers, target)
    print(ret)