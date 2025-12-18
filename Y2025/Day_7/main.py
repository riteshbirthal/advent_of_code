

class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)
        self.n, self.m = len(self.filtered_data), len(self.filtered_data[0])
        self.dp = [[-1]*self.m for _ in range(self.n)]

    def filter_data(self, data):
        return data
    
    def count_possibilities(self, x, y):
        if y<0 or y==self.m:
            return 0
        if x==self.n:
            return 1
        if self.dp[x][y] != -1:
            return self.dp[x][y]
        if self.filtered_data[x][y]=='^':
            self.dp[x][y] = self.count_possibilities(x+1, y-1) + self.count_possibilities(x+1, y+1)
        else:
            self.dp[x][y] = self.count_possibilities(x+1, y)
        return self.dp[x][y]
    
    def problem1(self):
        res = 0
        for i in range(1, self.n):
            for j in range(self.m):
                if self.filtered_data[i][j]=='^' and self.filtered_data[i-1][j] in ['S', '|']:
                    res += 1
                    if j-1 >= 0 and self.filtered_data[i][j-1]=='.':
                        self.filtered_data[i] = self.filtered_data[i][:j-1] + '|' + self.filtered_data[i][j:]
                    if j+1 < self.m and self.filtered_data[i][j+1]=='.':
                        self.filtered_data[i] = self.filtered_data[i][:j+1] + '|' + self.filtered_data[i][j+2:]
                elif self.filtered_data[i-1][j] in ['S', '|']:
                    self.filtered_data[i] = self.filtered_data[i][:j] + '|' + self.filtered_data[i][j+1:]
        return res

    def problem2(self):
        start_x, start_y = 0, 0
        for i in range(self.m):
            if self.filtered_data[0][i] == 'S':
                start_y = i
        res = self.count_possibilities(start_x+1, start_y)
        return res



