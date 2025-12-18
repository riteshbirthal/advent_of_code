

class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)

    def filter_data(self, data):
        filtered_data = [d.split('-') for d in data[0].split(',')]
        new_data = []
        for d in filtered_data:
            if len(d[0]) == len(d[1]):
                new_data.append([d[0], d[1]])
            else:
                diff = len(d[1]) - len(d[0])
                num1 = '9' * len(d[0])
                num2 = '1' + '0' * (len(d[1]) - 1)
                new_data.append([d[0], num1])
                for i in range(1, diff):
                    num_start = '1' + '0' * (len(d[0]) + i - 1)
                    num_end = '9' * (len(d[0]) + i)
                    new_data.append([num_start, num_end])
                new_data.append([num2, d[1]])
        return new_data
    
    def problem1(self):
        res = 0
        # print(self.filtered_data)
        for data in self.filtered_data:
            num1 = data[0][:len(data[0])//2] if len(data[0])>=2 else '1'
            # print(num1)
            while int(num1 + num1) <= int(data[1]):
                if int(num1 + num1) >= int(data[0]):
                    res += int(num1 + num1)
                num1 = str(int(num1) + 1)
        return res

    def problem2(self):
        res = 0
        for data in self.filtered_data:
            st = {}
            parts = 2
            while len(data[0])//parts:
                num1 = data[0][:len(data[0])//parts]
                if len(data[0]) % parts != 0:
                    parts += 1
                    continue
                while True:
                    num = num1
                    for i in range(parts - 1):
                        num += num1
                    if int(num) > int(data[1]):
                        break
                    # print(num)
                    if int(num) >= int(data[0]):
                        st[int(num)] = 1
                    num1 = str(int(num1) + 1)
                parts += 1
            # print("\n\n", data)
            keys = sorted(st.keys())
            for s in keys:
                # print(s)
                res += s
        return res