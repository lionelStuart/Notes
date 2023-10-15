def heap_sort(lst:list):
    for i in range(len(lst) // 2 - 1, -1, -1):
        heapify(lst, i, len(lst))

    for i in range(len(lst)-1, -1, -1):
        swap(lst, 0, i)
        heapify(lst, 0, i)

def heapify(lst:list, idx:int, n:int):
    left = 2*idx + 1
    right = 2*idx + 2
    large = idx
    if left < n and lst[left] > lst[large]:
        large = left
    if right < n and lst[right] > lst[large]:
        large = right
    if large != idx:
        swap(lst, large, idx)
        heapify(lst, large, n)

def swap(lst:list, a, b):
    tmp = lst[a]
    lst[a] = lst[b]
    lst[b] = tmp



if __name__ == '__main__':
    lst = [2,6,5,1,9,0,4,5,4,3,2,2,0]
    heap_sort(lst)
    print(lst)