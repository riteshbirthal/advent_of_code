

class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)

    def filter_data(self, data):
        return data
    
    def locate_accesses(self, data):
        n, m = len(data), len(data[0])
        x = [-1, -1, -1, 0, 0, 1, 1, 1]
        y = [-1, 0, 1, -1, 1, -1, 0, 1]
        for i in range(n):
            for j in range(m):
                if data[i][j] == '.':
                    continue
                count = 0
                for k in range(8):
                    ni, nj = i + x[k], j + y[k]
                    if 0 <= ni < n and 0 <= nj < m and data[ni][nj] in ['@', 'x']:
                        count += 1
                if count < 4:
                    data[i] = data[i][:j] + 'x' + data[i][j+1:]
        return data
    
    def problem1(self):
        res = 0
        data = self.locate_accesses(self.filtered_data.copy())
        for row in data:
            res += row.count('x')
        return res
                

    def problem2(self):
        res = 0
        data = self.filtered_data.copy()
        while True:
            data = self.locate_accesses(data)
            count = 0
            for i in range(len(data)):
                for j in range(len(data[0])):
                    if data[i][j] == 'x':
                        count += 1
                        data[i] = data[i][:j] + '.' + data[i][j+1:]
            res += count
            if count == 0:
                break
        return res