from fastapi import APIRouter, HTTPException

from backend import service
from backend.models import (
    CreateGroupRequest,
    AddMemberRequest,
    LoginRequest
)
from backend.errors import (
    UserNotFoundError,
    GroupNotFoundError,
    AlreadyMemberError,
    InvalidGroupNameError,
    InvalidCredentialsError,
)


router = APIRouter()

@router.post("/login")
def login(login_request: LoginRequest):
    try:
        token = service.login(
            login_request.email,
            login_request.password
        )

        return {
            "token": token
        }

    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )

@router.get("/users/{user_id}/groups")
def get_groups(user_id: int):
    try:
        return service.get_groups_for_user(user_id)

    except UserNotFoundError as error:
        raise HTTPException(404, str(error))


@router.get("/groups/{group_id}")
def get_group(group_id: int):
    try:
        return service.get_group(group_id)

    except GroupNotFoundError as error:
        raise HTTPException(404, str(error))


@router.post("/groups", status_code=201)
def create_group(group: CreateGroupRequest):
    try:
        return service.create_group(group.name)

    except InvalidGroupNameError as error:
        raise HTTPException(400, str(error))


@router.post("/groups/{group_id}/members", status_code=201)
def add_member(group_id: int, member: AddMemberRequest):
    try:
        return service.add_member(group_id, member.user_id)

    except GroupNotFoundError as error:
        raise HTTPException(404, str(error))

    except UserNotFoundError as error:
        raise HTTPException(404, str(error))

    except AlreadyMemberError as error:
        raise HTTPException(409, str(error))