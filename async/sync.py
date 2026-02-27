# 동기 프로그래밍
# 호출자(caller)가 피호출자(callee)를 기다림
# 동기 발식의 문제 -> 대기를 하는 동안 다른 작업을 처리하지 못해서, 비효율적


import time


def hello():
    time.sleep(5)
    print("hello")


hello()
