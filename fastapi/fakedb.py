# -*- encoding: utf-8 -*-
'''
@Time    :   2025/05/08 10:17:12
@Author  :   47bwy
@Desc    :   None
'''

from passlib.context import CryptContext

fake_users_db = {
    "apri": {
        "username": "apri",
        "full_name": "Apri Cotli",
        "email": "apri@example.com",
        "hashed_password": "$2b$12$j1EOzo8i5cfcYPwJlAVqB.epXmjl5XCg6eF.69pLtefOujzKnUu3S",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
