from traceback import print_list
from sympy import trace
from leetcode.link import ListNode, build_list, print_list




class Solution:
    def swapPairs(self, head):
        guard = ListNode(-1)
        guard.next = head
        curr = guard
        while curr:
            if curr.next and curr.next.next:
                nx = None
                a = curr.next
                b = curr.next.next
                if b.next:
                    nx = b.next
                curr.next = b
                b.next = a
                a.next = nx
                curr = a
            else:
                curr = None
        return guard.next
        
if __name__ == '__main__':
    s = Solution()
    head = [1,2,3]
    root = build_list(head)
    ret = s.swapPairs(root)
    print_list(ret)