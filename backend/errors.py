class UserNotFoundError(Exception):
    def __init__(self):
        super().__init__("User not found")


class GroupNotFoundError(Exception):
    def __init__(self):
        super().__init__("Group not found")


class AlreadyMemberError(Exception):
    def __init__(self):
        super().__init__("User is already a member")


class InvalidGroupNameError(Exception):
    def __init__(self):
        super().__init__("Group name cannot be empty")

class InvalidCredentialsError(Exception):
    def __init__(self):
        super().__init__("Invalid email or password")