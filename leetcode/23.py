# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from leetcode.link import build_list, ListNode, print_list


# class Solution:
    
#     # 小顶堆, 先建小顶堆，每次将堆顶最小元素替换为她的下个元素，如果没有下一个元素，则缩小堆
#     def mergeKLists(self, lists):
#         h = list()
#         for i in lists:
#             if not i:
#                 continue
#             h.append(i)
#         for i in range(len(h) // 2 - 1, -1, -1):
#             self.heapify(h, i, len(h))

#         guard = ListNode(-1)
#         curr = guard
#         while len(h):
#             elem = h[0]
#             curr.next = elem
#             curr = curr.next
#             if elem.next:
#                 h[0] = elem.next
#                 self.heapify(h, 0, len(h))
#             else:
#                 self.swap(h, 0, len(h)-1)
#                 h = h[:-1]
#                 self.heapify(h, 0, len(h))
#             curr.next = None
#         return guard.next

#     def heapify(self, h, idx, n):
#         left = idx * 2 + 1
#         right = idx * 2 + 2
#         small = idx
#         if left < n and h[left] and h[left].val < h[small].val:
#             small = left
#         if right < n and h[right] and h[right].val < h[small].val:
#             small = right
#         if small != idx:
#             self.swap(h, small, idx)
#             self.heapify(h, small, n)
            
#     def swap(self, h, a, b):
#         tmp = h[a]
#         h[a] = h[b]
#         h[b] = tmp
        
class Solution:
    # 使用归并求解
    def mergeKLists(self, lists):
        if len(lists) == 0:
            return None
        n = len(lists)
        if n <=2:
            return self.merge2(lists)
        left = list()
        right = list()
        idx = 0
        while idx < len(lists):
            left.append(lists[idx])
            idx += 1
            if idx < len(lists):
                right.append(lists[idx])
                idx += 1
        # print(len(left))
        # print(len(right))
        a = self.mergeKLists(left)
        b = self.mergeKLists(right)
        return self.merge2([a, b])
        
    def merge2(self, lsts):
        if len(lsts) == 1:
            return lsts[0]
        idxa = lsts[0]
        idxb = lsts[1]
        guard = ListNode(-1)
        curr = guard
        while idxa or idxb:
            if idxa and idxb:
                if idxa.val <= idxb.val:
                    curr.next = idxa
                    curr = curr.next
                    idxa = idxa.next 
                else:
                    curr.next = idxb
                    curr = curr.next
                    idxb = idxb.next
            elif idxa:
                    curr.next = idxa
                    curr = curr.next
                    idxa = idxa.next 
            else:
                    curr.next = idxb
                    curr = curr.next
                    idxb = idxb.next
            curr.next = None
        # print_list(guard)
        return guard.next
        

    

if __name__ == '__main__':
    lists = [[1,4,5],[1,3,4],[2,6]]
    links = []
    for i in lists:
        tmp = build_list(i)
        links.append(tmp)
    s = Solution()
    ret = s.mergeKLists(links)
    print_list(ret)