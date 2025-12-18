

class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)
        self.visited = {}

    def filter_data(self, data):
        data = [d.split(': ') for d in data]
        filtered_data = {}
        for d in data:
            key = d[0]
            value = d[1].split(' ')
            filtered_data[key] = value
        return filtered_data
    
    def count_paths(self, node: str):
        if node in self.visited:
            return self.visited[node]
        if node == 'out':
            return 1
        total_paths = 0
        for neighbor in self.filtered_data.get(node, []):
            total_paths += self.count_paths(neighbor)
        self.visited[node] = total_paths
        return total_paths

    def count_paths_with_dac_and_fft_visits(self, node: str, dac_visited: bool, fft_visited: bool):
        if node == 'out':
            return 1 if dac_visited and fft_visited else 0
        key = (f"{node}-{dac_visited}-{fft_visited}")
        if key in self.visited: 
            return self.visited[key]
        total_paths = 0
        for neighbor in self.filtered_data.get(node, []):
            if neighbor == 'dac' and not dac_visited:
                total_paths += self.count_paths_with_dac_and_fft_visits(neighbor, True, fft_visited)
            elif neighbor == 'fft' and not fft_visited:
                total_paths += self.count_paths_with_dac_and_fft_visits(neighbor, dac_visited, True)
            elif neighbor not in ['dac', 'fft']:
                total_paths += self.count_paths_with_dac_and_fft_visits(neighbor, dac_visited, fft_visited)
        self.visited[key] = total_paths
        return total_paths
    
    def problem1(self):
        res = self.count_paths('you')
        return res

    def problem2(self):
        res = self.count_paths_with_dac_and_fft_visits('svr', False, False)
        return res