

class Problem:
    def __init__(self, data: list[str]):
        self.init_position = 50
        self.data = data
    
    def problem1(self):
        res = 0
        curr_position = self.init_position
        for d in self.data:
            curr_position = curr_position + int(d[1:]) if d[0]=='R' else curr_position - int(d[1:])
            curr_position = (curr_position + 100) % 100
            res = res + 1 if curr_position==0 else res
        return res

    def problem2(self):
        res = 0
        curr_position = self.init_position
        for d in self.data:
            n = int(d[1:])
            is_add = True if d[0]=='R' else False
            for i in range(n):
                curr_position = curr_position + 1 if is_add else curr_position - 1
                curr_position = (curr_position + 100)%100
                res = res + 1 if curr_position==0 else res
        return res