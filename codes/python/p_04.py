# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/03 14:57:29
@Author  :   47bwy
@Desc    :   None
'''

import time
from datetime import datetime, timedelta
from operator import itemgetter

rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]


rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print(rows_by_fname)
print(rows_by_uid)


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)


def sort_notcompare():
    users = [User(23), User(3), User(99)]
    print(users)
    print(sorted(users, key=lambda u: u.user_id))


sort_notcompare()


a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
a.update(b)
print(a)

t = time.time()
print(type(t), t)
time_struct = time.localtime(t)
print(type(time_struct), time_struct)
n = datetime.now()
print(type(n), n)
print(n.timestamp())
print(datetime.fromtimestamp(t))


from itertools import islice

items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):
    print(x)


items = ['a', 'b', 'c']

from itertools import combinations

for c in combinations(items, 3):
    print(c)
