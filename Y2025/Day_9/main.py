

class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)

    def filter_data(self, data):
        data = [d.split(',') for d in data]
        return data
    
    def problem1(self):
        res, n = 0, len(self.filtered_data)
        for i in range(n):
            for j in range(i+1, n):
                first_start, first_end = int(self.filtered_data[i][0]), int(self.filtered_data[i][1])
                second_start, second_end = int(self.filtered_data[j][0]), int(self.filtered_data[j][1])
                res = max(res, (abs(first_start - second_start) + 1) * (abs(first_end - second_end) + 1))
                
        return res

    def problem2(self):
        res = 0
        return res