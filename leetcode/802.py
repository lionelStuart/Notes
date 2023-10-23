class Solution:
    def eventualSafeNodes(self, graph):
        pass
        end = set()
        for idx in range(len(graph)):
            if len(graph[idx]) == 0:
                end.add(idx)
        
        while True:
            old_len = len(end)
            for idx in range(len(graph)):
                elem = graph[idx]
                tag = True
                for i in elem:
                    if i not in end:
                        tag = False
                        break
                if tag:
                    end.add(idx)
            if len(end) == old_len:
                break
        t = [i for i in end]
        t.sort()
        return t
    
        
if __name__ == '__main__':
    s = Solution()
    graph = [[],[0,2,3,4],[3],[4],[]]
    ret = s.eventualSafeNodes(graph)
    print(ret)