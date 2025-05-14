# -*- encoding: utf-8 -*-
'''
@Time    :   2025/05/08 12:17:00
@Author  :   47bwy
@Desc    :   None
'''

import bcrypt

# 新密码
new_password = "mypassword".encode()

# 自动生成 salt，并加密
hashed = bcrypt.hashpw(new_password, bcrypt.gensalt(rounds=12))

print(hashed.decode())