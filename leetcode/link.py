from tkinter import NO


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
        
def build_list(l:list):
    if len(l) == 0:
        return None
    root = ListNode(l[0])
    curr = root
    for i in range(1, len(l)):
        n = ListNode(l[i])
        curr.next = n
        curr = n
    return root 

def print_list(root):
    curr = root
    lst = list()
    while curr:
        lst.append(curr.val)
        curr = curr.next
    print(lst)
    
    
if __name__ == '__main__':
    l = [1,2,3,4,5,6]
    lst = build_list(l)
    print_list(lst)