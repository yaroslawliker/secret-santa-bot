import unittest
import datetime

from model import SecretSantaModel, User, LastSantaIsLastRecieverException

class TestSecretSantaModel(unittest.TestCase):

    def test_try_assign_santa(self):

        # Prepare data        
        model = SecretSantaModel()
        # u1 = User(chat_id=1, name="Alice")
        u2 = User(chat_id=2, name="Bob")
        u3 = User(chat_id=3, name="Charlie")

        santa = u2
        recievers = [u2, u3].copy()

        # Act
        reciever = model._try_assign_santa(santa, recievers)
        
        self.assertEqual(reciever, u3)
        self.assertEqual(recievers, [u2])

    def test_try_assign_santa_bad_try(self):

        # Prepare data        
        model = SecretSantaModel()
        u1 = User(chat_id=1, name="Alice")

        santa = u1
        recievers = [u1].copy()

        # Act
        with self.assertRaises(LastSantaIsLastRecieverException):
            reciever = model._try_assign_santa(santa, recievers)
        
        self.assertEqual(recievers, [u1])
    
    def test_try_map_santas_to_recievers(self):

        # Prepare data        
        model = SecretSantaModel()
        u1 = User(chat_id=10, name="Alice")
        u2 = User(chat_id=20, name="Bob")
        u3 = User(chat_id=30, name="Charlie")
        u4 = User(chat_id=40, name="Nick")
        u5 = User(chat_id=50, name="Yarko")
        u6 = User(chat_id=60, name="Anna")

        users_init = [u1, u2, u3, u4, u5, u6]
        users = users_init.copy()

        try:
            # Act
            santa_mappings = model._try_map_santas_to_recievers(users)
            givers = [mapping.giver for mapping in santa_mappings]
            receivers = [mapping.receiver for mapping in santa_mappings]
            
            # Assert all users are present as givers and receivers
            for user in users_init:
                self.assertIn(user, givers)
                self.assertIn(user, receivers)

            # Assert no same giver-reciever pairs
            for mapping in santa_mappings:
                self.assertNotEqual(mapping.giver.chat_id, mapping.receiver.chat_id)

            self.assertEqual(len(santa_mappings), 6)
            self.assertEqual(users_init, users)

        except LastSantaIsLastRecieverException as e:
            self.fail("LastSantaIsLastRecieverException was raised! It's OK! Just try again.")
        
        

    def test_assign_santas(self):
        # Prepare data        
        model = SecretSantaModel()
        u1 = User(chat_id=10, name="Alice")
        u2 = User(chat_id=20, name="Bob")
        u3 = User(chat_id=30, name="Charlie")
        u4 = User(chat_id=40, name="Nick")
        u5 = User(chat_id=50, name="Yarko")

        model.add_user(u1)
        model.add_user(u2)
        model.add_user(u3)
        model.add_user(u4)
        model.add_user(u5)

        # Act
        santa_mappings = model.assign_santas()

        givers = [mapping.giver for mapping in santa_mappings]
        receivers = [mapping.receiver for mapping in santa_mappings]

        # Assert all users are present as givers and receivers
        for user in [u1, u2, u3, u4, u5]:
            self.assertIn(user, givers)
            self.assertIn(user, receivers)
        
        # Assert no same giver-reciever pairs
        for mapping in santa_mappings:
            self.assertNotEqual(mapping.giver.chat_id, mapping.receiver.chat_id)
            print(f"{mapping.giver.name} -> {mapping.receiver.name}")






        