import vk_api

from random import randrange

from config import token_access_group

vk_session = vk_api.VkApi(token=token_access_group, api_version='5.131')

def send_some_msg(user_id, some_text, attachment = None):
    vk_session.method("messages.send", {
        "user_id": user_id,
        "message": some_text,
        "random_id": randrange(10 ** 7),
        "attachment": attachment
    })