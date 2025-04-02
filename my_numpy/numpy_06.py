# -*- encoding: utf-8 -*-
'''
@Time    :   2025/03/02 18:44:22
@Author  :   47bwy
@Desc    :   None
'''

import datetime
import socket
import struct

import numpy as np
from scapy.all import sniff

prices = [20, 18, 14, 17, 20, 21, 15]

def profit_1(prices):
    n = len(prices)
    max_profit = 0
    for i in range(n):
        for j in range(i, n):
            if prices[j] - prices[i] > max_profit:
                max_profit = prices[j] - prices[i]
    return max_profit

def profit_2(prices):
    max_px = 0
    min_px = prices[0]
    for px in prices[1:]:
        min_px = min(min_px, px)
        max_px = max(px - min_px, max_px)
    return max_px

# print(profit_1(prices))
# print(profit_2(prices))

# 捕获一个网络数据包
packet = sniff(count=1)[0]
# 将数据包转换为二进制数据
packet_bytes = bytes(packet)
print(packet_bytes)

# 将二进制数据转换为 numpy 数组
packet_array = np.frombuffer(packet_bytes, dtype=np.uint8)

# 解析各个字段
timestamp = np.frombuffer(packet_array[:4].tobytes(), dtype=np.uint32)[0]
src_ip = np.frombuffer(packet_array[4:8].tobytes(), dtype=np.uint32)[0]
dst_ip = np.frombuffer(packet_array[8:12].tobytes(), dtype=np.uint32)[0]
src_port = np.frombuffer(packet_array[12:14].tobytes(), dtype=np.uint16)[0]
dst_port = np.frombuffer(packet_array[14:16].tobytes(), dtype=np.uint16)[0]
payload = packet_array[16:].tobytes()

def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack('!I', ip_int))

timestamp = datetime.datetime.fromtimestamp(timestamp)
src_ip = int_to_ip(src_ip)
dst_ip = int_to_ip(dst_ip)
# 打印解析结果
print(f"Timestamp: {timestamp}")
print(f"Source IP: {src_ip}")
print(f"Destination IP: {dst_ip}")
print(f"Source Port: {src_port}")
print(f"Destination Port: {dst_port}")
print(f"Payload: {payload}")