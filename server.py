from fastapi import FastAPI, HTTPException
import csv


app = FastAPI()


# --------------------------------------------------
# GET all groups belonging to a user
# --------------------------------------------------

@app.get("/users/{user_id}/groups")
def get_groups(user_id: int):

    # First check whether the user actually exists
    user_exists = False

    with open("users.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["id"]) == user_id:
                user_exists = True
                break

    if not user_exists:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Find which groups this user belongs to
    memberships = []

    with open("memberships.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["user_id"]) == user_id:
                memberships.append(row)

    # Get the actual information about those groups
    groups = []

    with open("groups.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            for membership in memberships:

                if int(row["id"]) == int(membership["group_id"]):
                    groups.append({
                        "id": int(row["id"]),
                        "name": row["name"],
                        "balance": float(membership["balance"])
                    })

    return groups


# --------------------------------------------------
# GET one particular group
# --------------------------------------------------

@app.get("/groups/{group_id}")
def get_group(group_id: int):

    with open("groups.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if int(row["id"]) == group_id:
                return {
                    "id": int(row["id"]),
                    "name": row["name"]
                }

    raise HTTPException(
        status_code=404,
        detail="Group not found"
    )


# --------------------------------------------------
# CREATE a new group
# --------------------------------------------------

@app.post("/groups", status_code=201)
def create_group(group: dict):

    name = group.get("name")

    # Validate input
    if name is None or name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Group name cannot be empty"
        )

    # Find an ID for the new group
    largest_id = 0

    with open("groups.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            largest_id = max(largest_id, int(row["id"]))

    new_id = largest_id + 1

    # Store the new group
    with open("groups.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([new_id, name])

    return {
        "id": new_id,
        "name": name
    }


# --------------------------------------------------
# ADD a user to a group
# --------------------------------------------------

@app.post("/groups/{group_id}/members", status_code=201)
def add_member(group_id: int, member: dict):

    user_id = member.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="user_id is required"
        )

    # Check that the group exists
    group_exists = False

    with open("groups.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["id"]) == group_id:
                group_exists = True
                break

    if not group_exists:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    # Check that the user exists
    user_exists = False

    with open("users.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["id"]) == user_id:
                user_exists = True
                break

    if not user_exists:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Make sure they're not already in the group
    with open("memberships.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (
                int(row["group_id"]) == group_id
                and int(row["user_id"]) == user_id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="User is already a member"
                )

    # Add membership
    with open("memberships.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([group_id, user_id, 0])

    return {
        "group_id": group_id,
        "user_id": user_id,
        "balance": 0
    }
