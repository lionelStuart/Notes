
from leetcode.link import *

class Solution:
    # 删除链表倒数第N节点，哨兵节点+递归+递归后数值处理
    def removeNthFromEnd(self, head, n: int):
        guard = ListNode(-1)
        guard.next = head
        self.traverse(guard, n)
        return guard.next
                    
                    
    def traverse(self, head, n):
        if head.next is None:
            return 1
        if head.next:
            cnt = self.traverse(head.next, n)
        cnt += 1
        if cnt == n+1:
            head.next = head.next.next
        return cnt
    
if __name__ == '__main__':
    s = Solution()
    head = [1,2,3,4,5]
    n = 5
    l = build_list(head)
    r = s.removeNthFromEnd(l, n)
    print_list(r)