class Solution:
    # 合法括号 栈
    def isValid(self, s: str) -> bool:
        m = dict()
        m[')'] = '('
        m[']'] = '['
        m['}'] = '{'
        stk = list()
        for i in s:
            if len(stk) == 0:
                stk.append(i)
                continue
            if i in m and m[i] == stk[-1]:
                stk.pop()
            else:
                stk.append(i)
        return len(stk) == 0

if __name__ == '__main__':
    s = Solution()
    st = "(]"
    print(s.isValid(st))