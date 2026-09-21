from fastapi import FastAPI, HTTPException

from models import CreateGroupRequest, AddMemberRequest
import repository


app = FastAPI()


# --------------------------------------------------
# GET all groups belonging to a user
# --------------------------------------------------

@app.get("/users/{user_id}/groups")
def get_groups(user_id: int):

    user = repository.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    memberships = repository.get_memberships_for_user(user_id)
    all_groups = repository.get_groups()

    groups = []

    for membership in memberships:
        for group in all_groups:
            if int(group["id"]) == int(membership["group_id"]):
                groups.append({
                    "id": int(group["id"]),
                    "name": group["name"],
                    "balance": float(membership["balance"])
                })

    return groups


# --------------------------------------------------
# GET one particular group
# --------------------------------------------------

@app.get("/groups/{group_id}")
def get_group(group_id: int):

    group = repository.get_group(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    return {
        "id": int(group["id"]),
        "name": group["name"]
    }


# --------------------------------------------------
# CREATE a new group
# --------------------------------------------------

@app.post("/groups", status_code=201)
def create_group(group: CreateGroupRequest):

    name = group.name

    if name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Group name cannot be empty"
        )

    return repository.create_group(name)


# --------------------------------------------------
# ADD a user to a group
# --------------------------------------------------

@app.post("/groups/{group_id}/members", status_code=201)
def add_member(group_id: int, member: AddMemberRequest):

    user_id = member.user_id

    group = repository.get_group(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    user = repository.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if repository.membership_exists(group_id, user_id):
        raise HTTPException(
            status_code=409,
            detail="User is already a member"
        )

    return repository.add_membership(group_id, user_id)