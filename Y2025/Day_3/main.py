

class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)

    def filter_data(self, data):
        dp = []
        for d in data:
            prev_ele, n = {0 : '', 1 : d[-1]}, len(d)
            for i in range(n-1, -1, -1):
                l = n - i
                ele = prev_ele.copy()
                for j in range(1, l):
                    ele[j] = max(ele[j], d[i] + prev_ele[j-1])
                ele[l] = d[i] + prev_ele[l-1]
                prev_ele = ele.copy()
            dp.append(prev_ele)
        return dp
    
    def problem1(self):
        res = 0
        for i in range(len(self.filtered_data)):
            res += int(self.filtered_data[i][2])
        return res

    def problem2(self):
        res = 0
        for i in range(len(self.filtered_data)):
            res += int(self.filtered_data[i][12])
        return res