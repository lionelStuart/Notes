class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = self
        self.next = self
        
class EasyLink:
    # 有哨兵的双端队列，头尾指针都是哨兵节点会更简单
    # 需要实现队头出，队尾进，任意节点删除和尾节点判定
    def __init__(self):
        self.root = ListNode(-1,-1)
        self.root.next = self.root
        self.root.prev = self.root
        self.tail = self.root
        
        
    def push(self, n:ListNode):
        self.tail.next = n 
        n.prev = self.tail
        n.next = None 
        self.tail = n
    
    def remove(self, n:ListNode):
        prev = n.prev
        next = n.next 
        prev.next = next 
        next.prev =prev
        
    def move_tail(self, n:ListNode):
        self.remove(n)
        self.push(n)
        
    def is_tail(self, n):
        return n==self.tail
    
    def pop_front(self):
        if self.tail == self.root:
            return None
        if self.root.next == self.tail:
            old = self.root.next
            self.root.next = self.root
            self.root.prev = self.root
            self.tail = self.root
            return old
        else:   
            old = self.root.next
            self.root.next = old.next
            old.next.prev = self.root
            return old
            
    def print(self):
        curr = self.root
        if self.tail == self.root:
            return
        val = []
        while curr:
            val.append(curr.key)
            curr = curr.next
        print(val)

class LRUCache:
    # LRU 难顶， hash加双向队列
    # get 操作:
    # 无，返回-1，有返回值，如果非队尾节点则调整
    # put 操作:
    # 存在键，修改并调整队列
    # 不存在，如果队列满则移除旧值，增加新值，未满则队尾添加
    def __init__(self, capacity: int):
        self.m = dict()
        self.l = EasyLink()
        self.cap = capacity
        self.sz = 0

    def get(self, key: int) -> int:
        if key not in self.m:
            return -1
        tgt = self.m[key]
        if self.l.is_tail(tgt):
            return tgt.value
        self.l.move_tail(tgt)        
        return tgt.value
        

    def put(self, key: int, value: int) -> None:
        if self.sz == self.cap and key not in self.m:
            old = self.l.pop_front()
            if old:
                del(self.m[old.key])       
            nw = ListNode(key, value)
            self.l.push(nw)
            self.m[key] = nw
            return 
        if key in self.m:
            tgt = self.m[key]
            tgt.value = value
            if self.l.is_tail(tgt):
                return
            self.l.move_tail(tgt)
            return 
        nw = ListNode(key, value)
        self.l.push(nw)
        self.m[key] = nw
        self.sz += 1
        
    def print(self):
        self.l.print()
# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

if __name__ == '__main__':
    lru = LRUCache(2)
    lru.put(2,1)
    lru.print()
    lru.put(2,2)
    lru.print()
    lru.get(2)
    lru.print()
    lru.put(1,2)
    lru.print()
    lru.put(4,1)
    lru.get(2)
    lru.print()
    