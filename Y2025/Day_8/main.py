

class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)
        self.distances = self.compute_distances(self.filtered_data)
        self.parents = { '-'.join(node) : '-'.join(node) for node in self.filtered_data}
        self.group_size = { '-'.join(point) : 1 for point in self.filtered_data }
        self.max_group_size = 1
        self.last_X_prod_value = 0

    def filter_data(self, data):
        data = [d.split(',') for d in data]
        return data
    
    def compute_distances(self, data):
        new_data = {}
        n = len(data)
        for i in range(n):
            for j in range(i+1, n):
                [x1, y1, z1] = list(map(int, data[i]))
                [x2, y2, z2] = list(map(int, data[j]))
                dist = (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
                if dist not in new_data:
                    new_data[dist] = []
                new_data[dist].append([data[i], data[j]])
        return new_data

    def find_parent(self, node):
        if node not in self.parents:
            self.parents[node] = node
        if self.parents[node] != node:
            self.parents[node] = self.find_parent(self.parents[node])
        return self.parents[node]
    
    def problem1(self):
        res, pair_count = 1, 0
        distances = sorted(self.distances.keys())
        for dist in distances:
            edges = self.distances[dist]
            for e in edges:
                [u, v] = e
                if pair_count == 1000:
                    break
                pu, pv = self.find_parent('-'.join(u)), self.find_parent('-'.join(v))
                if pu != pv:
                    # print(f"  Considering edge between {u} and {v}")
                    self.parents[pu] = pv
                    self.group_size[pv] += self.group_size[pu]
                    if self.max_group_size != len(self.filtered_data):
                        self.last_X_prod_value = int(u[0]) * int(v[0])
                    self.max_group_size = max(self.max_group_size, self.group_size[pv])
                else:
                    # print(f"  Skipping edge between {u} and {v} as they are already connected")
                    pass
                pair_count += 1
            if pair_count == 1000:
                break
        groups = {}
        for node in self.filtered_data:
            parent = self.find_parent('-'.join(node))
            groups[parent] = self.group_size.get(parent, 0)
        values = sorted(groups.values(), reverse=True)[:min(3, len(groups))]
        for val in values:
            res *= val
        return res

    def problem2(self):
        res = self.last_X_prod_value
        distances = sorted(self.distances.keys())
        for dist in distances:
            edges = self.distances[dist]
            if self.max_group_size == len(self.filtered_data):
                break
            for e in edges:
                [u, v] = e
                pu, pv = self.find_parent('-'.join(u)), self.find_parent('-'.join(v))
                if pu != pv:
                    # print(f"  Considering edge between {u} and {v}")
                    self.parents[pu] = pv
                    self.group_size[pv] += self.group_size[pu]
                    if self.max_group_size != len(self.filtered_data):
                        res = int(u[0]) * int(v[0])
                    self.max_group_size = max(self.max_group_size, self.group_size[pv])
                else:
                    # print(f"  Skipping edge between {u} and {v} as they are already connected")
                    pass
                if self.max_group_size == len(self.filtered_data):
                    break
        return res