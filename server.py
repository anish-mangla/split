import repository

from errors import (
    UserNotFoundError,
    GroupNotFoundError,
    AlreadyMemberError,
    InvalidGroupNameError,
)


def get_groups_for_user(user_id: int):

    user = repository.get_user(user_id)

    if user is None:
        raise UserNotFoundError()

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


def get_group(group_id: int):

    group = repository.get_group(group_id)

    if group is None:
        raise GroupNotFoundError()

    return {
        "id": int(group["id"]),
        "name": group["name"]
    }


def create_group(name: str):

    if name.strip() == "":
        raise InvalidGroupNameError()

    return repository.create_group(name)


def add_member(group_id: int, user_id: int):

    group = repository.get_group(group_id)

    if group is None:
        raise GroupNotFoundError()

    user = repository.get_user(user_id)

    if user is None:
        raise UserNotFoundError()

    if repository.membership_exists(group_id, user_id):
        raise AlreadyMemberError()

    return repository.add_membership(group_id, user_id)