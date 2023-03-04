"""Меняет в БД значение appeal(кол-во обращений пользователя) на 1 больше"""
from database import get_appeal_user, appeal_update
def update_appeal(user_id):
    appeal_old = ((get_appeal_user(user_id))[0])  # возвращает предыдущее кол-во обращений пользователя
    appeal_new = (appeal_old + 1)  # увеличивает кол-во обращений на 1
    appeal_update(user_id, appeal_new)  # записывает в БД увеличенное кол-во  обращений