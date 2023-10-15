def quick_sort(lst:list):
    qsort(lst, 0, len(lst)-1)

def partiton(lst:list, st:int, et:int):
    mid = lst[st]
    left =st
    right = et
    while left < right:
        while left < right and lst[right] >= mid:
            right -= 1
        if left < right:
            lst[left] = lst[right]
        while left < right and lst[left] < mid:
            left += 1
        if left < right:
            lst[right] = lst[left]
    lst[left] = mid
    return left

def qsort(lst:list, st:int, et:int):
    p = partiton(lst, st, et)
    if p - 1 > st:
        qsort(lst, st, p-1)
    if p + 1 < et:
        qsort(lst, p+1, et)

def swap(lst:list, a, b):
    tmp = lst[a]
    lst[a] = lst[b]
    lst[b] = tmp

if __name__ == '__main__':
    lst = [2,6,5,1,9,0,4,5,4,3,2,2,0]
    quick_sort(lst)
    print(lst)