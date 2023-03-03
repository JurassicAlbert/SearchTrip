from typing import Dict


class RequestUserData:
    def __init__(self, data: Dict[str, str]):
        self.username = data.get('username')
        self.password = data.get('password')
