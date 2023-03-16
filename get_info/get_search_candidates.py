from config import token_user
import vk_api

from bot import send_some_msg

from get_info.validator import validator_try
from get_info.get_age_info import get_age
from get_info.get_photo_info import photo_info
from database import availability_candidate, add_candidate, get_id_user_table

''' Возвращает список кандидатов с открытым профилем  и указанной полной датой рождения в ВК
    в соответствии с заданным критерием поиска.
    '''
def search_candidates(par, user_id):
    sex = par[0]
    age_at = par[1]
    age_to = par[2]
    city = par[3]
    offset = ((par[4]-1) * 5) #при повторном поиске смещает поиск от первоначального на шаг 5
    if sex == 1:
        sex_search = 2
    else:
        sex_search = 1

    print(f'параметры поиска candidates: sex/age_at/age_to/city_id/offset: {sex_search}, {age_at}, {age_to}, {city}, '
          f'{offset}')

    sorted_candidates_response = {}
    full_candidates = {}
    link_profile = 'https://vk.com/id'
    vk = vk_api.VkApi(token=token_user)

    candidates_response = vk.method('users.search', {
                                                    'sort': 0,
                                                    'sex': sex_search,
                                                    'status': 6,
                                                    'age_from': age_at,
                                                    'age_to': age_to,
                                                    'offset': offset,
                                                    'has_photo': 1,
                                                    'count': 5,
                                                    'city': city,
                                                    'fields': 'sex, bdate, city, has_photo, status'
                                                    })

    if validator_try(candidates_response, 'items') is False:
        print('ошибка candidates_response')
        return None
    for item in candidates_response['items']:
        if item['is_closed'] is False and len(item['bdate']) > 7 and photo_info(item['id']) is not False:
            if (availability_candidate(item['id']) is False): #проверка на наличие в таблице candidates
                age_candidate = get_age(item['bdate'])  # определяет возраст candidate
                for key, value in item.items():
                    if key == 'city':
                        sorted_candidates_response['city_id'] = value['id']
                        sorted_candidates_response['city_title'] = value['title']
                    # На случай, когда метод users.search выдает ответ без city в candidates_response
                    # (иногда выдает такой вариант, при условии, что город поиска был задан),
                    # запишет данные о городе candidate как None
                    elif 'city' not in item:
                        sorted_candidates_response = dict.fromkeys(['city_title', 'city_id'])
                sorted_candidates_response['id_candidate'] = item['id']
                sorted_candidates_response['first_name'] = item['first_name']
                sorted_candidates_response['last_name'] = item['last_name']
                sorted_candidates_response['sex'] = item['sex']
                sorted_candidates_response['age'] = age_candidate
                sorted_candidates_response['link_pro'] = link_profile + str(item['id'])
                send_some_msg(user_id, f'Профиль кандидата для просмотра:')
                send_some_msg(user_id, (link_profile + str(item['id'])))
                photo = photo_info(item['id'])[0] #1е фото с максммальной суммой лайков и коментариев
                sorted_candidates_response['url_photo_1'] = photo
                send_some_msg(user_id, f'Фото профиля по популярности №1:', photo)
                photo = photo_info(item['id'])[1] #2е фото с максммальной суммой лайков и коментариев
                sorted_candidates_response['url_photo_2'] = photo
                send_some_msg(user_id, f'Фото профиля по популярности №2:', photo)
                photo = photo_info(item['id'])[2] #3е фото с максммальной суммой лайков и коментариев
                sorted_candidates_response['url_photo_3'] = photo
                send_some_msg(user_id, f'Фото профиля по популярности №3:', photo)
                send_some_msg(user_id, f'----------------')
                id_table = (get_id_user_table(user_id)[0])  # id таблицы users_of_VKinder пользователя
                sorted_candidates_response['user_id_table'] = id_table
                print(f'данные для записи в БД в таблицу candidates: {sorted_candidates_response}')
                full_candidates[candidates_response['items'][0]['id']] = sorted_candidates_response
                add_candidate(full_candidates)  # передаём список в db для записи информации о candidate

    if candidates_response.get('items'):
        return False
