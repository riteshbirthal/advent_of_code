filename = "input.txt"

with open(filename, 'r') as file:
    data = file.readlines()

data = [d.split('\n')[0] for d in data]

# for d in data:
#     print(len(d))
res = 0
n, m = len(data), len(data[0])
# print(n, m)

for i in range(1, n):
    for j in range(m):
        # print(i, j, n, m)
        if data[i][j]=='^' and data[i-1][j] in ['S', '|']:
            res += 1
            if j-1 >= 0 and data[i][j-1]=='.':
                data[i] = data[i][:j-1] + '|' + data[i][j:]
            if j+1 < m and data[i][j+1]=='.':
                data[i] = data[i][:j+1] + '|' + data[i][j+2:]
        elif data[i-1][j] in ['S', '|']:
            data[i] = data[i][:j] + '|' + data[i][j+1:]
print(res)

dp = []
for d in data:
    dp.append([-1]*len(d))

# print(data)
def count_possibilities(x, y):
    if y<0 or y==m:
        return 0
    if x==n:
        return 1
    # print(x, y, dp[x][y])
    if dp[x][y] != -1:
        return dp[x][y]
    if data[x][y]=='^':
        dp[x][y] = count_possibilities(x+1, y-1) + count_possibilities(x+1, y+1)
    else:
        dp[x][y] = count_possibilities(x+1, y)
    return dp[x][y]

start_x, start_y = 0, 0
for i in range(m):
    if data[0][i] == 'S':
        start_y = i

res = count_possibilities(start_x+1, start_y)
print(res)
