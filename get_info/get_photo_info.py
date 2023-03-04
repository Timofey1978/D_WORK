from config import token_user

import vk_api

from config import token_access_group

vk_session = vk_api.VkApi(token=token_access_group, api_version='5.131')

def photo_info(candidate_id):
    ''' Возвращает топ-3 популярных фотографий профиля.
        Популярность определяется по количеству лайков и комментариев(их сумме).
        '''
    dict_for_sort = {}

    vk = vk_api.VkApi(token=token_user)
    photos = vk.method('photos.get', {
                                        'owner_id': candidate_id,
                                        'album_id': 'profile',
                                        'extended': 1
                                        })
    if photos['count'] < 3:
        return False

    for item in photos['items']:
        dict_for_sort[item['id']] = (item['likes']['count'] + item['comments']['count'])
    sorted_tuples = sorted(dict_for_sort.items(), key=lambda item: item[1])

    sort = sorted_tuples[-3::]
    attachment1 = f'photo{candidate_id}_{sort[0][0]}'
    attachment2 = f'photo{candidate_id}_{sort[1][0]}'
    attachment3 = f'photo{candidate_id}_{sort[2][0]}'

    return attachment1, attachment2, attachment3