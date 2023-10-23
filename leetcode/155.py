class MinStack:
    # 最小栈，能用O1时间获取当前最小值的栈
    # 双栈，其中一个栈顶入当前最小值
    def __init__(self):
        self.stk = list()
        self.min_stk = list()

    def push(self, val: int) -> None:
        if len(self.stk) == 0:
            self.stk.append(val)
            self.min_stk.append(val)
            return
        mi = min(self.min_stk[-1], val)
        self.stk.append(val)
        self.min_stk.append(mi)
        
    def pop(self) -> None:
        self.stk.pop()
        self.min_stk.pop()
        
    def top(self) -> int:
        if len(self.stk) == 0:
            return -1
        return self.stk[-1]

    def getMin(self) -> int:
        return self.min_stk[-1]