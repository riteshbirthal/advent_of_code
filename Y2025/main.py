import re
import Y2025.Day_1.main as d1
import Y2025.Day_2.main as d2
import Y2025.Day_3.main as d3
import Y2025.Day_4.main as d4
import Y2025.Day_5.main as d5
import Y2025.Day_6.main as d6
import Y2025.Day_7.main as d7
import Y2025.Day_8.main as d8
import Y2025.Day_9.main as d9
import Y2025.Day_10.main as d10
import Y2025.Day_11.main as d11
import Y2025.Day_12.main as d12

PackageMappings = {
    1 : d1,
    2 : d2,
    3 : d3,
    4 : d4,
    5 : d5,
    6 : d6,
    7 : d7,
    8 : d8,
    9 : d9,
    10: d10,
    11: d11,
    12: d12
}
    

class AoC:
    def __init__(self):
        pass

    def read_input(self, day: int):
        file_path = f"./Day_{day}/input.txt"
        data = []
        with open(file_path, 'r') as file:
            data = file.readlines()
        return [d.split('\n')[0] for d in data]

    def _normalize_input_text(self, raw: str) -> list[str]:
        """Normalize raw input text:
        - Normalize line endings
        - Remove thousands separators inside numbers (e.g., 62,817 -> 62817)
        - Strip BOM and surrounding whitespace
        - Return non-empty lines
        """
        if raw is None:
            return []
        # Normalize line endings
        s = raw.replace('\r\n', '\n').replace('\r', '\n')
        # Remove BOM if present
        s = s.lstrip('\ufeff')
        # Split into lines and strip whitespace
        lines = [ln.strip() for ln in s.split('\n')]
        # Filter out purely empty lines
        return [ln for ln in lines if ln != '']

    def solve_problem(self, day: int, data=None):
        """Solve a day's problems.

        Parameters
        - day: day number
        - data: optional input; if None, read from `Day_<n>/input.txt`. If str, will be split onlines; if list, used directly.
        """
        if data is None:
            lines = self.read_input(day)
        elif isinstance(data, str):
            lines = self._normalize_input_text(data)
        else:
            joined = '\n'.join([str(x) for x in data])
            lines = self._normalize_input_text(joined)

        prob = PackageMappings[day].Problem(lines)
        try:
            part1 = prob.problem1()
            part2 = prob.problem2()
        except ValueError as e:
            # Re-raise with context so callers can show a helpful message
            raise ValueError(f"Error while running day {day}: {e}")

        return {"day": day, "part1": part1, "part2": part2}
    

if __name__=="__main__":
    aoc = AoC()
    days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for day in days:
        result = aoc.solve_problem(day)
        print(f"Solution for AoC Day {result['day']} problem 1 is: {result['part1']}")
        print(f"Solution for AoC Day {result['day']} problem 2 is: {result['part2']}")
