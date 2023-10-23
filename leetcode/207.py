
class Solution:
    # 拓扑排序，课程间存在依赖关系，判断能否修完课程
    # 即回环检测
    # 先用邻接列表形式改写图
    # 然后使用DFS遍历查找回环, trace集合用于判断是否访问本连接上的节点
    # 优化方法，用visited集合表示访问的节点，其子节点被访问或者没有子节点时才可以加入visited集合
    # （1）遍历入口处对visited集合过滤
    # （2）DFS内部对visited集合做过滤，访问到visited集合说明已处理过，则不进入递归
    
    # BFS 解法，统计入度为0的节点，每次仅通过入度0节点，并扩大入度范围，将原入度0节点标为
    # visited, 如果BFS结束后还有节点不在visited中，则为环中的节点
    
    # 如果不存在，输出[], 如果存在，输出合理的顺序
                # if i not in self.seq:
                #     self.seq.append(i)
    # 在所有visited中增加上述代码，visited顺序即倒序输出的DFS顺序
    
    def canFinish(self, numCourses: int, prerequisites):
        m = dict()
        for edge in prerequisites:
            s, e = edge[0], edge[1]
            if s not in m:
                m[s] = [e]
            else:
                m[s].append(e)

        visited = set()
        self.seq = list()
        for i in range(numCourses):
            if i not in m:
                # if i not in self.seq:
                #     self.seq.append(i)
                visited.add(i)
                continue
            trace = set()
            v = self.dfs(m, i, trace, visited)
            if not v:
                return []
        # print(self.seq)
        return self.seq
    
    def dfs(self, m, i, trace, visited):
        if i in trace:
            return False
        trace.add(i)
        if i not in m:
            # if i not in self.seq:
            #     self.seq.append(i)
            visited.add(i)
            trace.add(i)
            return True
        for next in m[i]:
            if  next in visited:
                continue
            t = trace.copy()
            if not self.dfs(m, next, t, visited):
                return False
        # if i not in self.seq:
        #     self.seq.append(i)
        visited.add(i)
        return True
        
                    


if __name__ == '__main__':
    s = Solution()
    numCourses = 2
    prerequisites = [[1,0]]
    # prerequisites = [[1,0],[2,0],[2,1],[3,1],[3,2],[4,2],[4,3],[5,3],[5,4],[6,4],[6,5],[7,5],[7,6],[8,6],[8,7],[9,7],[9,8],[10,8],[10,9],[11,9],[11,10],[12,10],[12,11],[13,11],[13,12],[14,12],[14,13],[15,13],[15,14],[16,14],[16,15],[17,15],[17,16],[18,16],[18,17],[19,17],[19,18],[20,18],[20,19],[21,19],[21,20],[22,20],[22,21],[23,21],[23,22],[24,22],[24,23],[25,23],[25,24],[26,24],[26,25],[27,25],[27,26],[28,26],[28,27],[29,27],[29,28],[30,28],[30,29],[31,29],[31,30],[32,30],[32,31],[33,31],[33,32],[34,32],[34,33],[35,33],[35,34],[36,34],[36,35],[37,35],[37,36],[38,36],[38,37],[39,37],[39,38],[40,38],[40,39],[41,39],[41,40],[42,40],[42,41],[43,41],[43,42],[44,42],[44,43],[45,43],[45,44],[46,44],[46,45],[47,45],[47,46],[48,46],[48,47],[49,47],[49,48],[50,48],[50,49],[51,49],[51,50],[52,50],[52,51],[53,51],[53,52],[54,52],[54,53],[55,53],[55,54],[56,54],[56,55],[57,55],[57,56],[58,56],[58,57],[59,57],[59,58],[60,58],[60,59],[61,59],[61,60],[62,60],[62,61],[63,61],[63,62],[64,62],[64,63],[65,63],[65,64],[66,64],[66,65],[67,65],[67,66],[68,66],[68,67],[69,67],[69,68],[70,68],[70,69],[71,69],[71,70],[72,70],[72,71],[73,71],[73,72],[74,72],[74,73],[75,73],[75,74],[76,74],[76,75],[77,75],[77,76],[78,76],[78,77],[79,77],[79,78],[80,78],[80,79],[81,79],[81,80],[82,80],[82,81],[83,81],[83,82],[84,82],[84,83],[85,83],[85,84],[86,84],[86,85],[87,85],[87,86],[88,86],[88,87],[89,87],[89,88],[90,88],[90,89],[91,89],[91,90],[92,90],[92,91],[93,91],[93,92],[94,92],[94,93],[95,93],[95,94],[96,94],[96,95],[97,95],[97,96],[98,96],[98,97],[99,97]]
    ret = s.canFinish(numCourses, prerequisites)
    print(ret)