class Node:
    def __init__(self, val) -> None:
        self.val = val
        self.next = []
        self.flag = False


class Trie:
    # 前缀树实现，重点在实现遍历方法，类似与链表遍历查看前缀相同
    def __init__(self):
        self.root = Node('')

    def insert(self, word: str) -> None:
        head, idx = self.traverse(word)
             
        for i in range(idx, len(word)):
            nw = Node(word[i])
            head.next.append(nw)
            head = nw
        head.flag = True

    def search(self, word: str) -> bool:
        if len(word) == 0:
            return False
        head, idx = self.traverse(word)
                    
        return idx == len(word) and head.flag is True

    def startsWith(self, prefix: str) -> bool:
        if len(prefix) == 0:
            return False
        head, idx = self.traverse(prefix)
        return idx == len(prefix) 
    
    def traverse(self, word):
        head = self.root
        idx = 0
        while idx < len(word):
            find = False
            for i in head.next:
                if i.val == word[idx]:
                    head = i
                    idx += 1
                    find = True
                    break
            if not find:
                break   
        return head, idx
        
    
if __name__ == '__main__':
    trie = Trie()
    trie.insert("apple")
    print(trie.search("apple"))   # 返回 True
    print(trie.search("app"))     # 返回 False
    print(trie.startsWith("app")) # 返回 True
    trie.insert("app")
    print(trie.search("app"))     # 返回 True