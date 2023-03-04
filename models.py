import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users_of_VKinder(Base):
    __tablename__ = 'users_of_VKinder'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)

    vk_user_id = sq.Column(sq.Integer)
    appeal = sq.Column(sq.Integer) #количество обращений пользователя к боту
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    param_sex = sq.Column(sq.Integer)
    param_relation = sq.Column(sq.Integer)
    param_age = sq.Column(sq.Integer)
    param_min_age = sq.Column(sq.Integer)
    param_max_age = sq.Column(sq.Integer)
    param_city_name = sq.Column(sq.String)
    param_city_id = sq.Column(sq.Integer)
    link_pro = sq.Column(sq.String)

class Candidates(Base):
    __tablename__ = 'candidates'

    id = sq.Column(sq.Integer, primary_key=True)
    id_users_of_VKinder = sq.Column(sq.Integer, sq.ForeignKey("users_of_VKinder.id"), nullable=False)

    vk_id_candidates = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    param_sex = sq.Column(sq.Integer)
    param_age = sq.Column(sq.Integer)
    param_city_name = sq.Column(sq.String)
    param_city_id = sq.Column(sq.Integer)
    url_photo_1 = sq.Column(sq.String)
    url_photo_2 = sq.Column(sq.String)
    url_photo_3 = sq.Column(sq.String)
    link_pro = sq.Column(sq.String)

    users_of_VKinder = relationship(Users_of_VKinder, backref="candidates")

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)