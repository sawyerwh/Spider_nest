
import time
import threading
# 定义一个全局变量
g_num = 0
# # 创建一个互斥锁
mutex = threading.Lock()


def test1(num):
    global g_num
    # 上锁
    # mutex.acquire()
    for i in range(num):
        g_num += 1
    #解锁
    # mutex.release()
    print('---test1--%d---' % g_num)
    # time.sleep(1)


def test2(num):
    global g_num
    # 上锁
    # mutex.acquire()
    for i in range(num):
        g_num += 1
    # 解锁
    # mutex.release()
    print('---test2--%d---' % g_num)
    # time.sleep(1)


def main():
    # 显示当前运行 线程 列表
    print(threading.enumerate())
    t1 = threading.Thread(target=test1, args=(10000,))
    t2 = threading.Thread(target=test2, args=(10000,))

    t1.start()
    t2.start()

    # 等待上面2个子线程结束...
    time.sleep(2)
    print('---in main Thread g_num = %d---' % g_num)


if __name__ == '__main__':
    main()
