# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/01 14:16:31
@Author  :   47bwy
@Desc    :   None
'''

import sched
import time

s = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
    print(f"Time: {time.ctime()}, Arg: {a}")

# 定时执行，带优先级
s.enter(10, 1, print_time, argument=('priority_10s',))  # 10秒后，优先级1
s.enter(5, 3, print_time, argument=('priority_3',))   # 5秒后，优先级3
s.enter(5, 1, print_time, argument=('priority_1',))   # 5秒后，优先级1
s.enter(5, 2, print_time, argument=('priority_2',))   # 5秒后，优先级2

s.run()


