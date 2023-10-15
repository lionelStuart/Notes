class Solution:
    # 最大岛屿面积， DFS
    def maxAreaOfIsland(self, grid) -> int:

        m = len(grid)
        n = len(grid[0])
        tmp = [0 for i in range(n)]
        mat = [tmp.copy() for j in range(m)]
        sz = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    continue
                if mat[i][j] != 0:
                    continue
                v = self.dfs(grid, mat, i, j, m, n)
                if v:
                    sz = max(sz, v)
        return sz
         
    def dfs(self, grid, mat, i, j, m, n):
        if i < 0 or i == m:
            return 0
        if j < 0 or j == n:
            return 0
        if grid[i][j] and not mat[i][j]:
            mat[i][j] = 1
            c1 = self.dfs(grid, mat, i-1, j, m, n)
            c2 = self.dfs(grid, mat, i+1, j, m, n)
            c3 = self.dfs(grid, mat, i, j-1, m, n)
            c4 = self.dfs(grid, mat, i, j+1, m, n)
            print('good')
            return c1 + c2 + c3 + c4 + 1
        return 0
                
                
            
    
    
if __name__ == '__main__':

    s = Solution()
    grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
    ret = s.maxAreaOfIsland(grid)
    print(ret)