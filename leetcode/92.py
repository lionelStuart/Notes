# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

from operator import le
from re import S
from leetcode.link import *

class Solution:
    # 反转指定位置的链表节点，先遍历到指定位置，取前驱后驱节点，再反转中间的链表节点
    def reverseBetween(self, head, left: int, right: int):
        guard = ListNode(-1)
        guard.next = head

        curr = guard
        pleft = None
        pright = None
        cnt = 0
        while curr:
            cnt += 1
            if cnt == left:
                pleft = curr
            if cnt == right:
                pright = curr.next
            curr = curr.next
        if pright:
            tmp = pright.next
            if tmp:
                pright.next = None
            pright = tmp
        head, root = self.reverse(pleft.next)
        pleft.next = head
        if root:
            root.next = pright
        return guard.next
        
                
    def reverse(self, head):
        if not head.next:
            return head, head
        beg, end = self.reverse(head.next)
        end.next = head
        head.next = None
        end = head
        return beg, end
    
if __name__ == '__main__':
    head = [1,2,3,4,5]
    left = 2
    right = 4
    
    head = [5]
    left = 1
    right = 1
    
    t = build_list(head)
    s = Solution()
    ret = s.reverseBetween(t, left, right)
    print_list(ret)