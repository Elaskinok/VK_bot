"""Vk bot (wtf, what i have to write here ??? )."""

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from yandex_parse import chart_as_string
from db_users import UsersDB

import random

ASSESSMENTS = ['You are beautiful', 'You look well',
               'You look wonderful', 'You have beautiful eyes',
               'You are looking so lovely'
               ]

HELLO_MSG = 'Hi! Im a bot. You can send a message to me.'
BUTT_TEXT_ASSESMENT = 'Get assessment of pic'
BUTT_TEXT_CHART = 'Get Yandex Chart'
NOT_EXIST_PHOTO_MSG = "Ooh...I'm sorry, but you don't have main photo :("
UNKNOWN_MSG = 'Unknown message...'


class VKBot:
    """Logic model of vk_bot."""

    def __init__(self):
        """Constructor.

        init neccessery members as:
            token: need to connect with group of VK
            keyboard_json: users will use keyboard for work with bot
            db: DataBase in which will write info about users,
                which will use bot

            OTHERS: need to work with vk's API
        """
        self.token = open('token.txt', 'r').read()
        self.keyboard = open("buttons.json", 'r', encoding="UTF-8").read()
        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()
        self.db = UsersDB()

    def send_img(self, user_id: int, photo_id: str) -> None:
        """Send image with photo_id and assessment about it to user with user_id."""
        self.vk.messages.send(user_id=user_id,
                              attachment='photo{}'.format(photo_id),
                              message=ASSESSMENTS[
                                  random.randint(0,
                                                 len(ASSESSMENTS) - 1)
                              ],
                              random_id='0')

    def answer_user(self, user_id: int, message: str) -> None:
        """Send text message to user with user_id."""
        self.vk.messages.send(user_id=user_id,
                              message=message,
                              random_id='0',
                              keyboard=self.keyboard)

    def about_user(self, user_id: int) -> {}:
        """Return information about user with user_id."""
        return self.vk.users.get(user_ids=user_id,
                                 fields='photo_id, screen_name',
                                 name_case='Nom')[0]

    def listen(self) -> None:
        """Wait messages from user and reacts to it."""
        for event in self.longpoll.listen():
            if (event.type == VkEventType.MESSAGE_NEW and
                    event.to_me and event.text):

                # out info about user to console
                print(f"From user: \"{event.text}\"")
                print(self.about_user(event.user_id))

                # push user's info to DataBase
                self.db.push_user(self.about_user(event.user_id), event.text)

                if event.text == 'Начать' or event.text == 'Start':
                    self.answer_user(event.user_id, HELLO_MSG)
                elif event.text == BUTT_TEXT_ASSESMENT:
                    if self.about_user(event.user_id).get('photo_id', '') is not '':
                        self.send_img(event.user_id,
                                      self.about_user(event.user_id)['photo_id']
                                      )
                    else:
                        self.answer_user(event.user_id, NOT_EXIST_PHOTO_MSG)
                elif event.text == BUTT_TEXT_CHART:
                    self.answer_user(event.user_id, chart_as_string())
                elif event.text == 'stop':
                    break
                else:
                    self.answer_user(event.user_id, UNKNOWN_MSG)
