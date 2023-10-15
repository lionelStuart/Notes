class Solution:
    # 岛屿周长，行扫描
    def islandPerimeter(self, grid) -> int:
        m = len(grid)
        n = len(grid[0])
        sz = 0
        near = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    sz +=1
        
        for i in range(m):
            for j in range(1, n):
                if grid[i][j-1] == 1 and grid[i][j] == 1:
                    near +=1 
                
        for i in range(n):
            for j in range(1, m):
                if grid[j-1][i] == 1 and grid[j][i] == 1:
                    near +=1 

        return sz* 4 - near*2
    
if __name__ == '__main__':

    s = Solution()
    grid = [[1,1],[1,1]]

    ret = s.islandPerimeter(grid)
    print(ret)