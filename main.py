import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token_access_group

from update_appeal_user import update_appeal
from database import parametr_search_city, parametrs_search, city_ad_db
from get_info.get_user_info import users_get
from get_info.get_city_info import city_info
from get_info.get_search_candidates import search_candidates
from bot import send_some_msg

vk_session = vk_api.VkApi(token=token_access_group, api_version='5.131')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id
        if msg == "начать" or msg == "hi" or msg == "hello" or msg == "привет" or msg == "хай":
            users_get(user_id)
            name = users_get(user_id)[1]
            if parametr_search_city(user_id) is False:
                print('город не указан в профиле')
                send_some_msg(user_id, f'Привет, {name}, на твоей странице не указан город проживания, '
                                       f'введи название города, например:    Москва    , '
                                       f'затем введи    ПОИСК   для подбора пары')
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        msg = event.text.lower()
                        city_add = city_info(msg) #передаёт название города в get_city_info, возвращает словарь id и title города
                        #если была ошибка, то повторно запрашивает название города
                        if city_add is False:
                            send_some_msg(user_id, f'{name}, некорректно указан город, '
                                                    f'введи название города, например:    Москва    , '
                                                   f'затем введи    ПОИСК   для подбора пары')
                        else:
                            city_ad_db(city_add, user_id) #добавляет в БД недостающие данные по городу(from database import city_ad_db)
                            break
            else:
                print('город указан в профиле')
                send_some_msg(user_id, f'Привет,{name}, введи  ПОИСК   для подбора пары')
        elif msg == "поиск":
            par = parametrs_search(user_id)
            print(f'параметры пользователя: sex/min_age/max_age/city_id/appeal: {par}')
            search_candidates(par, user_id)
            if search_candidates(par, user_id) is False:#возвращает значение, когда поиск подходящих candidates закончен
                print('candidates подобраны')
                update_appeal(user_id) #обновляет в таблице пользователя кол-во обращений
                send_some_msg(user_id, f'Бот  VKinder подобрал тебе варианты, просмотри их,'
                                       f'если хочешь больше вариантов, то введи    ПОИСК    , '
                                       f'если хочешь завершить, то введи    ВЫХОД')
        elif msg == "выход":
            send_some_msg(event.user_id, "Пока... :))")
            break
        else:
            send_some_msg(event.user_id, "бот VKinder не понял твоего ответа... :))")
