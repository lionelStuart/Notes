class Solution:
    # 没有完全PASS，迷宫，求最近出口距离，用BFS，记录访问节点和每个节点的步数，步数取最小值
    def nearestExit(self, maze, entrance) -> int:
        self.m = len(maze)
        self.n = len(maze[0])
        tmp = [0 for i in range(self.n)]
        self.visited = [tmp.copy() for i in range(self.m)]
        tmp = [self.m*self.n for i in range(self.n)]
        self.step = [tmp.copy() for i in range(self.m)]
        self.step[entrance[0]][entrance[1]] = 0
        self.entrace = entrance
        self.ret = list()  
        self.bfs(maze, entrance[0], entrance[1])

        if len(self.ret) == 0:
            return -1
        mi = self.step[self.ret[0][0]][self.ret[0][1]]
        val = self.ret[0]
        for i in self.ret:
            mx = self.step[i[0]][i[1]]
            if mx < mi:
                mi = mx
                val = i
        # print('ret=',self.ret, self.step)
        return mi   
        
        
    def bfs(self, maze, i, j):
        nx = [[i,j+1], [i,j-1],[i-1,j],[i+1,j]]
        tgt = list()
        if self.visited[i][j] == 1:
            return 
        self.visited[i][j] = 1      
        for p in nx:
            if p[0]< 0 or p[0]>= self.m:
                continue
            if p[1]<0 or p[1]>= self.n:
                continue

            if maze[p[0]][p[1]] == '+':
                self.visited[p[0]][p[1]] = 1
                continue
            self.step[p[0]][p[1]] = min(self.step[i][j] + 1, self.step[p[0]][p[1]])
            # print('step=',  self.step)
            # print('visited=', self.visited)

            
            if p[0] == 0 or p[0] == (self.m-1) or p[1] == 0 or p[1] == (self.n-1):
                # print('cand=',p)
                if p[0] != self.entrace[0] or p[1] != self.entrace[1]:
                    self.ret.append(p)
            tgt.append(p)
        # print(' ')
        for i in tgt:
            self.bfs(maze, i[0], i[1])

        
        
    
if __name__ == '__main__':
    maze = [["+","+","+"],[".",".","."],["+","+","+"]]
    entrance = [1,0]
    # entrance = [1,0]
    s = Solution()
    ret = s.nearestExit(maze, entrance)
    print(ret)