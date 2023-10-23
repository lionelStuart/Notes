class Solution:
    # 图，DAG搜索所有从0到达N-1可能路径， DFS
    def allPathsSourceTarget(self, graph):
        tmp = list()
        traces = self.dfs(graph, 0, tmp)
        ret = list()
        for i in traces:
            if i[-1] == len(graph)-1:
                ret.append(i)
        return ret
        
    def dfs(self, graph, i, trace):
        if i == len(graph)-1:
            trace.append(i)
            return [trace]
        
        ret = list()
        trace.append(i)
        for j in graph[i]:
            tmp = trace.copy()
            lst = self.dfs(graph, j, tmp)
            for p in lst:
                ret.append(p)
            
        return ret
    
if __name__ == '__main__':
    graph = [[1,2],[3],[3],[]]
    s = Solution()
    print(s.allPathsSourceTarget(graph))