from database import availability_user, add_user

import vk_api

from config import token_user

from get_info.get_age_info import get_age

''' Проверяет на наличие пользователя приложением VKinder в Базе Данных, 
    если пользователя в БД нет, то возвращает словарь с информацией о пользователе VKinder,
    после чего добавляет его в Базу Данных.
    Если информации недостаточно(город не указан в КОНТАКТАХ), то заносит информацию о городе в БД как None.
    '''
def users_get(user_id):
    all_user_info_response = {}
    full_user = {}
    link_profile = 'https://vk.com/id'

    vk = vk_api.VkApi(token=token_user)
    user_info_response = vk.method('users.get', {
                                                'user_ids': user_id,
                                                'fields': 'sex, bdate, city, relation'
                                                })
    print(user_info_response)

    name = user_info_response[0]['first_name']

    if availability_user(user_info_response[0]['id']) is False:  # возвращает значение на наличие пользователя в базе данных
        print('пользователя нет в БД')
        age_user = get_age(user_info_response[0]['bdate'])  # определяет возраст пользователя
        age_min = age_user - 5
        age_max = age_user + 2
        for key, value in user_info_response[0].items():
            if key == 'city':
                # если город в анкете не указан, то заносит None а данном этапе в БД
                all_user_info_response['city_id'] = value['id']
                all_user_info_response['city_title'] = value['title']
            elif 'city' not in user_info_response[0]:
                all_user_info_response = dict.fromkeys(['city_title', 'city_id'])
            all_user_info_response['id'] = user_info_response[0]['id']
            all_user_info_response['appeal'] = 1
            all_user_info_response['first_name'] = user_info_response[0]['first_name']
            all_user_info_response['last_name'] = user_info_response[0]['last_name']
            all_user_info_response['sex'] = user_info_response[0]['sex']
            all_user_info_response['relation'] = user_info_response[0]['relation']
            all_user_info_response['age'] = age_user
            all_user_info_response['min_age'] = age_min
            all_user_info_response['max_age'] = age_max
            all_user_info_response['link_pro'] = link_profile + str(user_info_response[0]['id'])
        full_user[user_info_response[0]['id']] = all_user_info_response
        add_user(full_user)  # передаём список в db для записи информации о пользавателе

    return full_user, name
