import repository


def get_groups_for_user(user_id: int):
    user = repository.get_user(user_id)

    if user is None:
        return None

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
    return repository.get_group(group_id)


def create_group(name: str):
    if name.strip() == "":
        return None

    return repository.create_group(name)


def add_member(group_id: int, user_id: int):

    group = repository.get_group(group_id)

    if group is None:
        return "GROUP_NOT_FOUND"

    user = repository.get_user(user_id)

    if user is None:
        return "USER_NOT_FOUND"

    if repository.membership_exists(group_id, user_id):
        return "ALREADY_MEMBER"

    return repository.add_membership(group_id, user_id)
