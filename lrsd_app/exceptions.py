class Password_or_username_none(Exception):
    def __init__(self) -> None:
        self.error = {}
        self.error["msg"] = "password or username is blank"

        super().__init__()
class Pass_user_incorrect(Exception):
    def __init__(self, error : dict) -> None:
        self.error = error or {}
        super().__init__()

class not_user(Exception):
    def __init__(self, error : dict) -> None:
        self.error = error or {}
        super().__init__()
    