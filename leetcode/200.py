class Solution:
    # 岛屿数量，DFS
    def numIslands(self, grid) -> int:
        pass
        m = len(grid)
        n = len(grid[0])
        tmp = [0 for i in range(n)]
        mat = [tmp.copy() for j in range(m)]
        cnt = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    continue
                if mat[i][j] != 0:
                    continue
                v = self.dfs(grid, mat, i, j, m, n)
                if v:
                    cnt +=1 
        return cnt
         
    def dfs(self, grid, mat, i, j, m, n):
        if i < 0 or i == m:
            return 0
        if j < 0 or j == n:
            return 0
        if grid[i][j] == "1" and not mat[i][j]:
            mat[i][j] = 1
            self.dfs(grid, mat, i-1, j, m, n)
            self.dfs(grid, mat, i+1, j, m, n)
            self.dfs(grid, mat, i, j-1, m, n)
            self.dfs(grid, mat, i, j+1, m, n)
            return 1
        return 0
                
                
            
    
    
if __name__ == '__main__':

    s = Solution()
    grid = [
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","1"]
    ]
    ret = s.numIslands(grid)
    print(ret)