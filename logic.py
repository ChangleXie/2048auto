import random


def new_game(n):
    return [[0] * n for i in range(n)]


def gen(mat):
    x, y = random.randint(0, len(mat) - 1), random.randint(0, len(mat) - 1)
    while mat[x][y] != 0:
        x, y = random.randint(0, len(mat) - 1), random.randint(0, len(mat) - 1)
    k = random.random()
    
    if k > 0.95:
        mat[x][y] = 4
    else:
        mat[x][y] = 2
    
    return mat


def game_state(mat, winnum):
    for item in mat:
        if winnum in item:
            return 'win'
    
    for i in range(len(mat)):
        for j in range(len(mat)):
            for m, n in [(0, 1), (1, 0)]:
                if m + i < len(mat) and n + j < len(mat) and mat[i][j] == mat[m + i][n + j] or mat[i][j] == 0:
                    return
    return 'lose'


def cover_up(mat):
    new = [[0] * len(mat) for i in range(len(mat))]
    done = False
    for i in range(len(mat)):
        count = 0
        for j in range(len(mat)):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


def merge(mat):
    done = False
    for i in range(len(mat)):
        for j in range(len(mat) - 1):
            if mat[i][j] == mat[i][j + 1] and mat[i][j]!=0:
                mat[i][j] *= 2
                mat[i][j + 1] = 0
                done = True
    return mat, done


def reverse_m(mat):
    return [list(reversed(i)) for i in mat]


def transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat))]


def left(mat):
    mat, done = cover_up(mat)
    temp = merge(mat)
    done = done or temp[1]
    mat = temp[0]
    mat = cover_up(mat)[0]
    return mat, done


def right(mat):
    mat = reverse_m(mat)
    mat, done = cover_up(mat)
    temp = merge(mat)
    done = done or temp[1]
    mat = temp[0]
    mat = cover_up(mat)[0]
    mat = reverse_m(mat)
    return mat, done


def up(mat):
    mat = transpose(mat)
    mat, done = cover_up(mat)
    temp = merge(mat)
    done = done or temp[1]
    mat = temp[0]
    mat = cover_up(mat)[0]
    mat = transpose(mat)
    return mat, done


def down(mat):
    mat = reverse_m(transpose(mat))
    mat, done = cover_up(mat)
    temp = merge(mat)
    done = done or temp[1]
    mat = temp[0]
    mat = cover_up(mat)[0]
    mat = transpose(reverse_m(mat))
    return mat, done
