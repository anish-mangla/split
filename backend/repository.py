import csv


def get_user(user_id: int):
    with open("users.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["id"]) == user_id:
                return row

    return None


def get_group(group_id: int):
    with open("groups.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["id"]) == group_id:
                return row

    return None


def get_groups():
    with open("groups.csv") as file:
        reader = csv.DictReader(file)
        return list(reader)


def get_memberships_for_user(user_id: int):
    memberships = []

    with open("memberships.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["user_id"]) == user_id:
                memberships.append(row)

    return memberships


def membership_exists(group_id: int, user_id: int):
    with open("memberships.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (
                int(row["group_id"]) == group_id
                and int(row["user_id"]) == user_id
            ):
                return True

    return False


def create_group(name: str):
    largest_id = 0

    with open("groups.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            largest_id = max(largest_id, int(row["id"]))

    new_id = largest_id + 1

    with open("groups.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([new_id, name])

    return {
        "id": new_id,
        "name": name
    }


def add_membership(group_id: int, user_id: int):
    with open("memberships.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([group_id, user_id, 0])

    return {
        "group_id": group_id,
        "user_id": user_id,
        "balance": 0
    }

def get_user_by_email(email: str):
    with open("users.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["email"] == email:
                return row

    return None