from fastapi import FastAPI, Path, Query, status, HTTPException, Depends
from typing import Optional
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest
from db_connection import SessionFactory, getSession
from db_models import User
from sqlalchemy import select


app = FastAPI()

users: list[dict] = [
    {"id": 1, "name": "Alice", "age": 30, "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "age": 25, "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "age": 35, "email": "charlie@example.com"},
    {"id": 4, "name": "David", "age": 40, "email": "david@example.com"},
]


@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def get_users_handlers(session=Depends(getSession)):
    stmt = select(User)
    result = session.execute(stmt)
    users = result.scalars().all()
    return users


# @app.get("/users/{user_id}")
# def get_user_handler(user_id: int):
#     return users[user_id - 1]


# 회원 검색 API
@app.get("/users/search")
def search_users_handler(name: str):
    return {"message": f"회원 검색 API입니다. 검색어: {name}"}


# 단일 사용자 조회 API
# 설정	의미
# gt	Greater Than (> 초과)
# ge	Greater than or Equal to (≥ 이상)
# lt	Less Than (< 미만)
# le	Less than or Equal to (≤ 이하)
# title	문서에 표시될 제목
@app.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse
)
def get_user_handler(
    user_id: int = Path(..., ge=1, description="사용자 ID는 1 이상이어야 합니다."),
    session=Depends(getSession),
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자 ID입니다."
        )
    return user


# 사용자 정보 수정 API
@app.put("/users/{user_id}")
def update_user_handler(
    body: UserUpdateRequest,
    user_id: int = Path(..., ge=1, description="사용자 ID는 1 이상이어야 합니다."),
    session=Depends(getSession),
):
    if body.name is None and body.age is None:
        raise HTTPException(status_code=400, detail="업데이트할 정보가 없습니다.")

    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자 ID입니다."
        )

    # 2) 사용자 정보 업데이트
    if body.name is not None:
        user.name = body.name
    if body.age is not None:
        user.age = body.age
    session.commit()

    # 3) 업데이트된 사용자 정보 반환
    return user


# 사용자 삭제(회원탈퇴) API
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_handler(
    user_id: int = Path(..., ge=1, description="사용자 ID는 1 이상이어야 합니다."),
    session=Depends(getSession),
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자 ID입니다."
        )

    session.delete(user)
    session.commit()
    return None


# 회원가입 API
@app.post(
    "/users/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def signup_user_handler(body: UserSignUpRequest, session=Depends(getSession)):
    # new_user = {
    #     "id": len(users) + 1,
    #     "name": body.name,
    #     "age": body.age,
    #     "email": body.email,
    #     "grade": "S",
    # }
    # users.append(new_user)
    # SQLAlchemy ORM을 통해 새로운 user 인스턴스 생성
    new_user = User(name=body.name, age=body.age, email=body.email)

    # DB 작업 단위
    session.add(new_user)  # 임시 저장
    session.commit()  # DB에 저장
    return new_user


# GET / items /{item_name}
# item_name: str & 최대 글자수(max_length) 6
items = [
    {"id": 1, "item_name": "apply"},
    {"id": 2, "item_name": "banana"},
    {"id": 3, "item_name": "cherry"},
]


# @app.get("/items/{item_name}")
# def get_item_handler(
#     item_name: str = Path(
#         ..., min_length=2, max_length=6, description="아이템 이름은 최대 6자입니다."
#     )
# ):
#     for item in items:
#         if item["item_name"] == item_name:
#             return item
#     return {"message": "아이템을 찾을 수 없습니다."}


@app.get("/items/search")
def search_items_handler(
    item_name: str = Query(
        ...,
        min_length=2,
        max_length=6,
        description="아이템 이름은 최대 6자입니다.",  # ... 필수값
    ),
    age: Optional[int] = Query(
        None, ge=0, description="나이는 0 이상이어야 합니다."
    ),  # Optional 선택값
):
    return item_name, age
