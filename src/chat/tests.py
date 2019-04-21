from hashlib import md5

from django.contrib.auth import get_user_model
from django.test import TestCase

from chat.models import ChatGroup


class ChatGroupTest(TestCase):
    def setUp(self) -> None:
        self.UserModel = get_user_model()
        self.user_a = self.UserModel.objects.create(username='user_a', id=100000)
        self.user_b = self.UserModel.objects.create(username='user_b', id=100001)
        self.user_c = self.UserModel.objects.create(username='user_c', id=100002)

    def test_create_chat_empty(self):
        before = ChatGroup.objects.count()
        ChatGroup.create_chat()
        self.assertEqual(ChatGroup.objects.count(), before + 1, msg="Method create_chat() "
                                                                    "doesn't creates instance.")

    def test_create_chat_one_user(self):
        chat_group = ChatGroup.create_chat(self.user_a)
        self.assertEqual(chat_group.users.count(), 1, msg="User is not set in the create_chat() method. "
                                                          "Check for add() method call.")
        self.assertEqual(chat_group.users.first(), self.user_a, msg="Wrong user has been set. "
                                                                    "Check entire create_chat() method.")

    def test_create_chat(self):
        self.UserModel.objects.create(username='user_d')
        chat_group = ChatGroup.create_chat(self.user_a, self.user_b, self.user_c)
        self.assertEqual(chat_group.users.count(), 3, msg="User is not set in the create_chat() method. "
                                                          "Check for add() method call.")
        self.assertQuerysetEqual(chat_group.users.all(), map(str, [self.user_a.id, self.user_b.id, self.user_c.id]),
                                 transform=lambda x: str(x.id), ordered=False,  msg="Wrong users has been set. Check "
                                                                                    "entire create_chat() method.")

    def test_create_chat_uuid_empty(self):
        chat_group = ChatGroup.create_chat()
        self.assertEqual(
            chat_group.uuid.replace('-', ''),
            'd41d8cd98f00b204e9800998ecf8427e',
            msg="Wrong group UUID. Check that make_uuid() "
                "uses md5 method and that create_chat() calls him."
        )

    def test_create_chat_uuid(self):
        chat_group = ChatGroup.create_chat(self.user_a, self.user_b, self.user_c)
        self.assertEqual(
            chat_group.uuid.replace('-', ''),
            md5(', '.join(map(str, [self.user_a.id, self.user_b.id, self.user_c.id])).encode()).hexdigest(),
            msg="Wrong group UUID. Check create_chat() method "
                "for correct arguments passing to make_uuid()."
        )

    def test_get_chats_by_users_strict(self):
        chat_group_ab = ChatGroup.create_chat(self.user_a, self.user_b)
        ChatGroup.create_chat(self.user_a, self.user_b, self.user_c)
        qs = ChatGroup.get_chats_by_users(self.user_a, self.user_b, strict=True, use_uuid=False)
        self.assertEqual(qs.count(), 1, msg="Method get_chats_by_users() should return "
                                            "chat only with exact user-set match. "
                                            "Check query to filtering users amount")
        self.assertEqual(qs.first(), chat_group_ab, msg="Wrong result. Check get_chats_by_users() method.")

    def test_get_chats_by_users_strict_use_uuid_negative(self):
        chat_group = ChatGroup.create_chat(self.user_a, self.user_b)
        chat_group.uuid = 0
        chat_group.save()
        qs = ChatGroup.get_chats_by_users(self.user_a, self.user_b, strict=True, use_uuid=True)
        self.assertEqual(qs.count(), 0, msg="Check get_chats_by_users() for correct filtering by UUID.")

    def test_get_chats_by_users_strict_use_uuid_positive(self):
        ChatGroup.create_chat(self.user_a, self.user_b)
        qs = ChatGroup.get_chats_by_users(self.user_a, self.user_b, strict=True, use_uuid=True)
        self.assertEqual(qs.count(), 1, msg="Wrong result. Check get_chats_by_users() "
                                            "method for correct UUID creating.")

    def test_get_chats_by_users(self):
        ChatGroup.create_chat(self.user_a, self.user_b)
        ChatGroup.create_chat(self.user_a, self.user_b, self.user_c)
        qs = ChatGroup.get_chats_by_users(self.user_a, self.user_b, strict=False, use_uuid=False)
        self.assertEqual(qs.count(), 2, msg="Method get_chats_by_users() should return all"
                                            "chats that includes provided user-set. "
                                            "Check query for passing all()")
