
def graph(graph):
    # 检测有向无环图中是否有环, DFS 深度遍历，访问路径结束后退栈
    visited = dict()
    for node in graph:
        if node in visited:
            continue
        m = dict()
        if dfs(graph, node, m, visited):
            return True
    return False



def dfs(graph, node, m, visited):
    if node in m:
        print(m, 'node=', node)
        return True
    m[node] = 1
    visited[node] = 1
    if node not in graph:
        return False
    for neighbor in graph[node]:
        s = m.copy()
        if dfs(graph, neighbor, s, visited):
            return True
    return False


if __name__ == '__main__':
    g = {
        'A':['B'],
        'B':['C'],
        'C':['E', 'D'],
        'E':['A'],
    }
    # g = {
    #     'A':['B'],
    #     'B':['C'],
    #     'C':['E', 'D'],
    #     'E':['D'],
    # }
    print(graph(g))