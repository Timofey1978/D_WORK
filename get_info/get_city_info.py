import vk_api
from config import token_user
from get_info.validator import validator_try
''' Возвращает ID и название города через msg(city_name) запрос у пользователя в main,
если город проживания не был указан.'''
def city_info(city_name):
    city_search = {}
    vk = vk_api.VkApi(token=token_user)
    city = vk.method('database.getCities', {
                                            'country_id': 1,
                                            'q': f'{city_name}',
                                            'need_all': 0,
                                            'count': 1
                                            })
    if validator_try(city, 'tems') is False or validator_try(city, 'count') is False:
        print('ошибка city key')
        return None
    # try:
    #     city = city['items']
    # except KeyError as e:
    #     print(f' ошибка {e}')
    #     city['items'] = None
    #     return False

    if city['count'] == 0:
        print('некорректно указан город')
        return False
    else:
        for item in city['items']:
            city_search['city_id'] = item['id']
            city_search['city_title'] = item['title']
        return city_search
