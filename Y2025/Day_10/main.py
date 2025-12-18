class Problem:
    def __init__(self, data: list[str]):
        self.filtered_data = self.filter_data(data)

    def filter_data(self, data):
        filtered_data = []
        for d in data:
            [e0, e1] = d.split('] ')
            [e0, e1, e2] = [e0[1:], e1.split(' {')[0].split(), e1.split('{')[1][:-1].split(',')]
            n = len(e0)
            board = [0 if e0[i] == '.' else 1 for i in range(n)]
            joltages = [int(e) for e in e2]
            buttons = []
            for e in e1:
                state = [0 for i in range(n)]
                for b in e[1:-1].split(','):
                    state[int(b)] = 1
                buttons.append(state)
            elements = [board, buttons, joltages]
            filtered_data.append(elements)
        return filtered_data
    
    def find_min_buttons(self, current_board, final_board, b_idx, buttons, dp):
        is_done = True
        for i in range(len(current_board)):
            is_done = is_done and (current_board[i] == final_board[i])
        if is_done:
            return 0
        if b_idx == len(buttons):
            return 1000
        key = (b_idx, tuple(current_board))
        if key in dp:
             return dp[key]
        res = self.find_min_buttons(current_board.copy(), final_board, b_idx + 1, buttons, dp)
        new_state = [current_board[i] ^ buttons[b_idx][i] for i in range(len(current_board))]
        res = min(res, 1 + self.find_min_buttons(
            new_state,
            final_board,
            b_idx + 1,
            buttons,
            dp
        ))
        dp[key] = res
        return res
    
    def find_min_buttons_with_joltages(self, b_idx, buttons, joltages, presses, dp=None):
        return 1
    
    def problem1(self):
        res = 0
        for data in self.filtered_data:
            board, buttons, _ = data
            dp = {}
            res += self.find_min_buttons([0 for _ in board], board, 0, buttons, dp)
        return res

    def problem2(self):
        res, idx = 0, 1
        for data in self.filtered_data:
            board, buttons, joltages = data
            val = self.find_min_buttons_with_joltages(0, buttons, joltages, presses=0, dp=None)
            # print(f"Intermediate val: {val} for case {idx}")
            res += val
            idx += 1
        return res