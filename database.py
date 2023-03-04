import sqlalchemy
from sqlalchemy.orm import sessionmaker
# from pprint import pprint

from config import connection_driver, login, password, host, port, name_db
from models import create_tables, Users_of_VKinder, Candidates

DSN = f'{connection_driver}://{login}:{password}@{host}:{port}/{name_db}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

''' Добавляет пользователя в Базу Данных'''
def add_user(full_user):
    for item in full_user.values():
        new_user_data = Users_of_VKinder(
                            vk_user_id=item['id'],
                            appeal=item['appeal'],
                            first_name=item['first_name'],
                            last_name=item['last_name'],
                            param_sex=item['sex'],
                            param_relation=item['relation'],
                            param_age=item['age'],
                            param_min_age=item['min_age'],
                            param_max_age=item['max_age'],
                            param_city_name=item['city_title'],
                            param_city_id=item['city_id'],
                            link_pro=item['link_pro']
                            )

        session.add(new_user_data)
    session.commit()

''' Добавляет condidate в Базу Данных'''
def add_candidate(full_candidate):
    for item in full_candidate.values():
        new_candidate_data = Candidates(
                            vk_id_candidates=item['id_candidate'],
                            id_users_of_VKinder=item['user_id_table'],
                            first_name=item['first_name'],
                            last_name=item['last_name'],
                            param_sex=item['sex'],
                            param_age=item['age'],
                            param_city_name=item['city_title'],
                            param_city_id=item['city_id'],
                            url_photo_1=item['url_photo_1'],
                            url_photo_2=item['url_photo_2'],
                            url_photo_3=item['url_photo_3'],
                            link_pro=item['link_pro']
                            )
        session.add(new_candidate_data)
    session.commit()


''' Возвращает значение True/False, при наличии/отсутствии в БД
     пользователя приложением VKinder по user_id.'''
def availability_user(user_id):
    for user in session.query(Users_of_VKinder).filter(
            Users_of_VKinder.vk_user_id == int(user_id)).all():
        return True
    return False

''' Возвращает значение True/False, при наличии/отсутствии в БД
     candidates по id_candidates.'''
def availability_candidate(id_candidates):
    for candidate in session.query(Candidates).filter(
            Candidates.vk_id_candidates == int(id_candidates)).all():
        return True
    return False

'''Возвращает параметр поиска по id города,
    True/False при наличии/отсутствии в БД'''
def parametr_search_city(user_id):
    for parametr_city in session.query(Users_of_VKinder).filter(
            (Users_of_VKinder.vk_user_id == int(user_id)) &
            (Users_of_VKinder.param_city_id == None)).all():
        return False
    return True

'''Возвращает параметры поиска из БД по полу, мин/макс возрасту
    и id города'''
def parametrs_search(user_id):
    for parametrs in session.query(Users_of_VKinder.param_sex, Users_of_VKinder.param_min_age,
                                    Users_of_VKinder.param_max_age, Users_of_VKinder.param_city_id,
                                    Users_of_VKinder.appeal).filter(Users_of_VKinder.vk_user_id == int(user_id)).all():
        return parametrs

''' Добавляет в БД название и id города'''
def city_ad_db(city_add, user_id):
    list = []
    for item in city_add:
        item_list = (item, city_add[item])
        list.append(item_list)
    id_table = session.query(Users_of_VKinder.id).filter(Users_of_VKinder.vk_user_id == int(user_id)).all()
    city = session.query(Users_of_VKinder).get(id_table[0])
    city.param_city_id = list[0][1]
    city.param_city_name = list[1][1]
    session.commit()

'''Возвращает значение id как sq.Column(sq.Integer, primary_key=True) пользователя, т.е.
 под каким номером в таблице пользователь приложением'''
def get_id_user_table(user_id):
    for get_id_table in session.query(Users_of_VKinder.id).filter(Users_of_VKinder.vk_user_id == int(user_id)).all():
        return get_id_table

'''Возвращает значение appeal, т.е. в какой раз пользователь обращается в приложение'''
def get_appeal_user(user_id):
    for get_appeal in session.query(Users_of_VKinder.appeal).filter(Users_of_VKinder.vk_user_id == int(user_id)).all():
        return get_appeal

''' Обнавляет в БД количество обращений appeal пользователя с id_user'''
def appeal_update(user_id, appeal):
    get_id_table = session.query(Users_of_VKinder.id).filter(Users_of_VKinder.vk_user_id == int(user_id)).all()
    appeal_table = session.query(Users_of_VKinder).get(get_id_table[0])
    appeal_table.appeal = appeal
    session.commit()

session.close()