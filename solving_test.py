import threading
import requests
import time

# 定义每个线程的执行逻辑
def solve_sudoku_thread(url, sudoku):
    response = requests.post(url, json={"sudokus": [sudoku]}, timeout=10)
    # 处理响应结果

# 性能测试函数
def performance_test(url, sudokus, num_threads):
    start_time = time.time()

    # 创建并启动多个线程
    threads = []
    for sudoku in sudokus:
        thread = threading.Thread(target=solve_sudoku_thread, args=(url, sudoku))
        thread.start()
        threads.append(thread)

    # 等待所有线程执行完毕
    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    print("Total time:", total_time)

# 配置测试参数
url = "http://localhost:5000/solve_sudokus"
sudokus = [
    [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]],
    [[0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 3], [0, 7, 4, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 2], [0, 8, 0, 0, 4, 0, 0, 1, 0], [6, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 7, 8, 0], [5, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0]]
]
num_threads = 10

# 进行性能测试
performance_test(url, sudokus, num_threads)