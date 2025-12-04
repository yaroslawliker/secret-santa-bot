from dataclasses import dataclass
import random

from messages import Language

@dataclass
class User:
    chat_id: int
    name: str
    language_code = Language.SANTA
    registered = False


class State:
    WAITING = "WAITING"
    FINISHED = "FINISHED"

@dataclass
class SantaMapping:
    giver: User
    receiver: User

class LastSantaIsLastRecieverException(Exception):
    pass

class SecretSantaModel:

    def __init__(self):
        self.state = State.WAITING
        self.users = {}

    def add_user(self, user: User):
        self.users[user.chat_id] = user

    def get_user(self, user_id: int) -> User:
        return self.users[user_id]

    def has_user(self, user_id: int) -> bool:
        return user_id in self.users
    
    
    def get_registered_user_names(self) -> list:
        return [user.name for user in self.get_registered_users()]
    
    def get_registered_users(self) -> list:
        return [user for user in self.users.values() if user.registered]
    
    
    def change_name(self, user_id: int, new_name: str):
        if user_id in self.users:
            self.users[user_id].name = new_name
    
    def assign_santas(self):
        """Returns"""

        users = self.get_registered_users()
        while True:
            try:
                santa_mappings = SecretSantaModel._try_map_santas_to_recievers(users)
                self.state = State.FINISHED
                return santa_mappings
            except LastSantaIsLastRecieverException as e:
                continue

    @staticmethod
    def _try_map_santas_to_recievers(users):
        """Tries to map santas to recievers. Raises LastSantaIsLastRecieverException if fails."""

        santas = users.copy()
        recievers = users.copy()

        random.shuffle(santas)
        random.shuffle(recievers)

        santa_mappings = []

        for santa in santas:

            # Moving the exception outside
            try:
                reciever = SecretSantaModel._try_assign_santa(santa, recievers)
                santa_mapping = SantaMapping(giver=santa, receiver=reciever)
                santa_mappings.append(santa_mapping)
            except LastSantaIsLastRecieverException as e:
                raise e
            
        return santa_mappings
                
    @staticmethod
    def _try_assign_santa(santa, recievers):
            """Chooses a reciever and removes it from the list. Raises LastSantaIsLastRecieverException if only reciever is santa himself."""

            if len(recievers) == 1 and recievers[0].chat_id == santa.chat_id:
                raise LastSantaIsLastRecieverException()

            while True:
                potential_reciever = random.choice(recievers)

                if potential_reciever.chat_id != santa.chat_id:
                    recievers.remove(potential_reciever)
                    return potential_reciever

                
