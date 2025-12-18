




class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)

    def filter_data(self, data):
        data = [d.split('\n')[0] for d in data if d!='\n' and d!='']
        ranges = [[int(d.split('-')[0]), int(d.split('-')[1])] for d in data if '-' in d]
        ids = [int(d) for d in data if '-' not in d]
        return [ranges, ids]
    
    def problem1(self):
        res = 0
        ranges, ids = self.filtered_data
        for id in ids:
            for r in ranges:
                if r[0] <= id <= r[1]:
                    res += 1
                    break
        return res

    def problem2(self):
        new_range = []
        ranges, ids = self.filtered_data
        ranges.sort()
        for r in ranges:
            if len(new_range)==0 or new_range[len(new_range)-1][1] < r[0]:
                new_range.append(r)
            else:
                new_range[len(new_range)-1][1] = max(new_range[len(new_range)-1][1], r[1])
        res = 0
        for r in new_range:
            res += r[1] - r[0] + 1
        return res
