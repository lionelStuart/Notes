

class Solution:
    # 判断二分图，图染色问题，染色为0的节点下个节点为1，直到遍历完成或遇到冲突节点
    def isBipartite(self, graph) -> bool:
        if len(graph) == 0:
            return False
        self.paint = [-1 for i in range(len(graph))]
        self.cnt = 0
        self.paint[0] = 0
        ret = True
        for i in range(len(graph)):
            if len(graph[i]) == 0:
                self.paint[i] = 0
                continue
            ret = self.bfs(graph, i)
            if not ret:
                return ret
        return ret
        
    def bfs(self, graph, idx):
        self.cnt += 1
        curr = self.paint[idx]
        if curr == -1:
            self.paint[idx] = 0
        next = 0 if curr == 1 else 1

        for n in graph[idx]:
            if self.paint[n] == -1:
                self.paint[n] = next
            elif self.paint[n] != next:
                return False
        if self.cnt >= len(graph):
            return True
        
        for n in graph[idx]:
            if not self.bfs(graph, n):
                return False
            # if self.cnt >= len(graph):
            #     return True
            # self.bfs(graph, n)
        return True


if __name__ == '__main__':
    s = Solution()
    graph = [[],[3],[],[1],[]]
    ret = s.isBipartite(graph)
    print(ret)