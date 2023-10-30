class Solution:
    def fib(self, n: int) -> int:
        f0 = 0
        f1 = 1
        if n == 0:
            return f0
        if n == 1:
            return f1
        for i in range (2, n+1):
            tmp = f0 + f1
            f0 = f1 
            f1 = tmp
        return f1