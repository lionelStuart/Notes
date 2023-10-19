# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    #验证链表是回文串，使用递归，从尾指针开始同步更新头指针位置
    def isPalindrome(self, head) -> bool:
        self.head = head
        v, h =  self.search(head)
        return v
    
    def search(self, head):
        if head.next is None:
            return head.val == self.head.val, self.head
        

        ret, old =  self.search(head.next)
        if not ret:
            return False, old.next
        
        nx = old.next
        return nx.val == head.val, nx
                    
if __name__ == '__main__':
    s = Solution()
    lst = [1,2,3,3,2,1]
    l = build_list(lst)
    print(s.isPalindrome(l))