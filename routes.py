from fastapi import APIRouter, HTTPException

import service
from models import CreateGroupRequest, AddMemberRequest
from errors import (
    UserNotFoundError,
    GroupNotFoundError,
    AlreadyMemberError,
    InvalidGroupNameError,
)


router = APIRouter()


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