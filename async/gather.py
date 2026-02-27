# gather = 모으다
import asyncio


async def hello():
    print("hello")


coro1 = hello()
coro2 = hello()


async def main():
    await asyncio.gather(coro1, coro2)


asyncio.run(main())

# [ 정리 ]
# 1. 코루틴은 동시에 같이 실행되기 위한 함수들이다.
# 2. 코루틴은 하나만 실행할거면, 굳이 비동기로 할 이유가 없다.
# 3. 비동기 문법을 쓰더라도, 실제 프로그램의 동작은 동기식으로 동작 할 수 있다.(조심)
# 4. 코루틴을 동시에 실행하는 방법은 gather()를 사용
