# -*- coding = utf-8 -*-
# @Time : 2023-9-17 16:19
# @Author : Lurume
# @File : jiugong.py
# @Software : PyCharm
from flask import jsonify
import random
from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import json
import time

history = []
shijian = []
history_answer = []
app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True
# Flask路由，渲染前端页面
#进入界面
@app.route('/')
def home():
    return render_template('first.html')

#难度选择界面
@app.route('/choose')
def choose():
    return render_template('choosing.html')

#生成简单难度的数独
@app.route('/generate_easy_sudoku')
def generate_easy_sudoku():
    sudoku, answer = generate_sudoku_task("easy")
    data = {
        'sudoku': sudoku,
        'answer': answer
    }
    return render_template('one.html', data=json.dumps(data))

#生成中等难度的数独
@app.route('/generate_medium_sudoku')
def generate_medium_sudoku():
    sudoku, answer = generate_sudoku_task("medium")
    data = {
        'sudoku': sudoku,
        'answer': answer
    }
    return render_template('one.html', data=json.dumps(data))

#生成困难难度的数独
@app.route('/generate_hard_sudoku')
def generate_hard_sudoku():
    sudoku, answer = generate_sudoku_task("hard")
    data = {
        'sudoku': sudoku,
        'answer': answer
    }
    return render_template('one.html', data=json.dumps(data))

#并发生成九个hard难度的数独
@app.route('/nine')
def nine():
    # 并发生成数独
    with ThreadPoolExecutor(max_workers=9) as executor:
        results = [executor.submit(generate_sudoku_task,"hard") for i in range(9)]
    sudokus, answers = [], []
    for result in results:
        sudoku, answer = result.result()
        sudokus.append(sudoku)
        answers.append(answer)
    data = {
        'sudokus': sudokus,
        'answers': answers
    }
    return render_template('nine.html', data=json.dumps(data))

#返回历史记录
@app.route('/get_history')
def get_history():
    data = {
        'history': history,
        'shijian': shijian,
        'history_answer': history_answer
    }
    return render_template('history.html', data=json.dumps(data))

@app.route('/solve_sudokus', methods=['POST'])
def solve_sudokus():
    request_data = request.get_json()
    sudokus = request_data['sudokus']
    # 并发处理数独求解任务
    start = time.time()
    with ThreadPoolExecutor(max_workers=9) as executor:
        results = [executor.submit(get_solutions, sudoku) for sudoku in sudokus]
    end = time.time()
    # 获取结果
    solutions = []
    for result in results:
        solutions.append(result.result())
    print(solutions)
    # 返回结果
    data = {
        'answers': solutions,
        'time': end - start
    }
    return jsonify(data)



#生成数独的主函数
def generate_sudoku_task(difficulty):
    # 创建一个空的9x9数独网格
    grid = [[0 for _ in range(9)] for _ in range(9)]

    # 填充对角线上的3x3子网格
    for i in range(0, 9, 3):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for j in range(3):
            for k in range(3):
                grid[i + j][i + k] = nums.pop()

    # 使用回溯法填充剩余的空格
    solve_sudoku(grid)

    # 随机移除一些数字作为题目
    if difficulty == 'easy':
        remove_count = random.randint(30, 40)
    elif difficulty == 'medium':
        remove_count = random.randint(40, 50)
    elif difficulty == 'hard':
        remove_count = random.randint(50, 60)
    else:
        remove_count = random.randint(30, 50)

    # 创建一个空的9x9数独网格用于答案
    answer = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            answer[i][j] = grid[i][j]
    for _ in range(remove_count):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = ' '

    #记录历史记录
    history.insert(0, grid)
    shijian.insert(0, str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    history_answer.insert(0, answer)
    return grid, answer

#获取输入题目的答案
def get_solutions(grid):
    # 寻找空格的位置
    row, col = find_empty_cell(grid)

    # 如果没有找到空格，说明数独已经解决
    if row == -1 and col == -1:
        return grid

    # 尝试填入数字
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num

            # 递归解决剩余的空格
            if solve_sudoku(grid):
                return grid

            # 如果递归未能解决数独，回溯并尝试下一个数字
            grid[row][col] = 0

    # 所有数字都尝试过了，无解
    return None


def solve_sudoku(grid):
    # 寻找空格的位置
    row, col = find_empty_cell(grid)

    # 如果没有找到空格，说明数独已经解决
    if row == -1 and col == -1:
        return True

    # 尝试填入数字
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num

            # 递归解决剩余的空格
            if solve_sudoku(grid):
                return True

            # 如果递归未能解决数独，回溯并尝试下一个数字
            grid[row][col] = 0

    # 所有数字都尝试过了，无解
    return False
# 并发处理数独求解任务
def concurrent_solve_sudoku(grids):
    results = []
    with ThreadPoolExecutor() as executor:
        # 提交每个数独求解任务给线程池
        for grid in grids:
            results.append(executor.submit(solve_sudoku, grid))

    # 获取求解结果
    solutions = []
    for result in results:
        solution = result.result()
        solutions.append(solution)

    return solutions


def find_empty_cell(grid):
    # 寻找数值为0的空格
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0 or grid[i][j] == ' ':
                return i, j
    return -1, -1


def is_valid(grid, row, col, num):
    # 检查所在行是否合法
    for i in range(9):
        if grid[i][col] == num:
            return False

    # 检查所在列是否合法
    for j in range(9):
        if grid[row][j] == num:
            return False

    # 检查所在3x3子网格是否合法
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True




if __name__ == '__main__':
    app.run()
