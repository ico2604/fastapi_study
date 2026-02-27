# await 키워드 = I/O 대기가 발생하는 순간, 실행권을 양보하는 키워드
import asyncio
import time
from datetime import datetime


# 동기식
def task_a():

    print(f"A시작 : {datetime.now()}")
    time.sleep(3)
    print(f"A끝 : {datetime.now()}")


def task_b():
    print(f"B시작 : {datetime.now()}")
    time.sleep(3)
    print(f"B끝 : {datetime.now()}")


# 비동기
async def coro_a():
    print(f"A시작 : {datetime.now()}")
    await asyncio.sleep(3)
    print(f"A끝 : {datetime.now()}")


async def coro_b():
    print(f"B시작 : {datetime.now()}")
    await asyncio.sleep(3)
    print(f"B끝 : {datetime.now()}")


async def coro_c():
    print(f"C시작 : {datetime.now()}")
    await asyncio.sleep(3)
    print(f"C끝 : {datetime.now()}")


async def main():
    a = coro_a()
    b = coro_b()
    c = coro_c()
    await asyncio.gather(a, b, c)


print("========= 동기 실행===========")
sync_start = time.time()
task_a()
task_b()
sync_end = time.time()
print(f"{sync_start - sync_end:.1f}초")

print("======= 비동기 실행===========")
async_start = time.time()
asyncio.run(main())
async_end = time.time()
print(f"{async_start - async_end:.1f}초")
