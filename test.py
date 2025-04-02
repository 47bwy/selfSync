# -*- encoding: utf-8 -*-
'''
@Time    :   2025/02/26 14:50:43
@Author  :   47bwy
@Desc    :   None
'''

import json
import logging
import random
import socket
import struct
import sys
import time
from functools import wraps

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
hander = logging.StreamHandler()
logger.addHandler(hander)


server_ip = '127.0.0.1'
server_port = 27000



def retry_on_output(target_output, max_retries=3, delay=5):
    """当函数返回特定输出时 重新执行函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                result = func(*args, **kwargs)
                if target_output in result[1]:
                    retries += 1
                    logger.error(f'Matched specific output: {target_output}, Retry count: {retries}/{max_retries}.')
                    wait_time = delay * (2 ** (retries - 1)) + random.randint(0, 5)
                    logger.info(f"wait {wait_time:.2f}s to retry ...")
                    time.sleep(wait_time)
                else:
                    return result
            raise Exception(f'Matched: {target_output}, max retries {max_retries} reached, no valid result obtained.')
        return wrapper
    return decorator

class BaseSSHClient:

    def __init__(self) -> None:
        self.client = None


    def my_send(self, msg):
        msg_bs = msg.encode('utf-8')
        msg_struct_len = struct.pack('i', len(msg_bs))
        logger.debug(f'send msg_bs_len: {len(msg_bs)}')
        self.client.send(msg_struct_len)
        logger.debug(f'send msg_bs: {msg_bs}')
        self.client.send(msg_bs)
            
    def my_recv(self):
        data = b""
        try:
            msg_struct_len = self.client.recv(4)
            msg_len = struct.unpack('i', msg_struct_len)[0]
            logger.debug(f'recv msg_len: {msg_len}')
            while True:
                if len(data) == msg_len:
                    break
                data += self.client.recv(msg_len)
        except struct.error as e:
            # 'unpack requires a buffer of 4 bytes'
            stderr = f'my_recv ERROR: {str(e)}'
            logger.error(stderr)
            data = stderr.encode('utf-8')
        except ConnectionResetError as e:
            logger.error(f"baseSSHClient ConnectionResetErro: {e}")
            
        logger.debug(f'recv data: {data[-100:]}')
        return data.decode('utf-8')

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))
        self.client.settimeout(5)


    def _create_remote_connect(self, data):
        """client 通过 socket 连接服务端, 让其执行命令
        """
        try:
            stdout = stderr = ""
            self.connect()
            login_info = json.dumps([data])
            self.my_send(login_info)
            msg = self.my_recv()
            stdout, stderr, text = json.loads(msg)
        except Exception as e:
            err_msg = f"_create_remote_connect: {str(e)}"
            logger.error(err_msg)
            text = stderr = err_msg
        finally:
            return stdout, stderr, text

    # @retry_on_output("baseSSHClient ERROR")
    def _exec_command(self, data):
        """带上设备及账户信息 发送命令
        """
        msg = json.dumps([data])
        self.my_send(msg)
        try:
            stdout = stderr = text = ""
            msg = self.my_recv()
            stdout, stderr, text = json.loads(msg)
        except socket.timeout:
            err_msg = "baseSSHClient ERROR: socket_timeout(1200s)"
            logger.error(err_msg)
            stderr = err_msg
        except json.JSONDecodeError as e:
            err_msg = f"baseSSHClient ERROR: recv_data JSONDecodeError"
            logger.error(err_msg)
            stderr = err_msg
        except Exception as e:
            err_msg = f"_exec_command ERROR: {str(e)}"
            logger.error(err_msg)
            stderr = err_msg
        finally:
            return stdout, stderr
        

    def close(self):
        self.client.close()


if __name__ == "__main__":
    obj = BaseSSHClient()
    stdout, stderr, text = obj._create_remote_connect('uname')
    print(111111, stdout, stderr, text)
    stdout, stderr = obj._exec_command('hostname')
    print(222222, stdout, stderr)