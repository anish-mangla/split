from backend import repository
from backend.errors import (
    UserNotFoundError,
    GroupNotFoundError,
    AlreadyMemberError,
    InvalidGroupNameError,
)


def get_groups_for_user(user_id):
    user = repository.get_user_by_id(user_id)

    if user is None:
        raise UserNotFoundError()

    return repository.get_groups_for_user(user_id)


def get_group(group_id):
    group = repository.get_group_by_id(group_id)

    if group is None:
        raise GroupNotFoundError()

    return group


def create_group(name):
    if not name or not name.strip():
        raise InvalidGroupNameError()

    return repository.create_group(name)


def add_member(group_id, user_id):
    group = repository.get_group_by_id(group_id)

    if group is None:
        raise GroupNotFoundError()

    user = repository.get_user_by_id(user_id)

    if user is None:
        raise UserNotFoundError()

    if repository.is_user_in_group(user_id, group_id):
        raise AlreadyMemberError()

    return repository.add_member(group_id, user_id)