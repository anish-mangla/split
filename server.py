from fastapi import FastAPI, HTTPException

from models import CreateGroupRequest, AddMemberRequest
import service


app = FastAPI()


@app.get("/users/{user_id}/groups")
def get_groups(user_id: int):

    groups = service.get_groups_for_user(user_id)

    if groups is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return groups


@app.get("/groups/{group_id}")
def get_group(group_id: int):

    group = service.get_group(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    return {
        "id": int(group["id"]),
        "name": group["name"]
    }


@app.post("/groups", status_code=201)
def create_group(group: CreateGroupRequest):

    new_group = service.create_group(group.name)

    if new_group is None:
        raise HTTPException(
            status_code=400,
            detail="Group name cannot be empty"
        )

    return new_group


@app.post("/groups/{group_id}/members", status_code=201)
def add_member(group_id: int, member: AddMemberRequest):

    result = service.add_member(
        group_id,
        member.user_id
    )

    if result == "GROUP_NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    if result == "USER_NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if result == "ALREADY_MEMBER":
        raise HTTPException(
            status_code=409,
            detail="User is already a member"
        )

    return result