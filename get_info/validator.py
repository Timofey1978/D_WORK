def validator_try(key, value):
    try:
        validator = key[value]
    except KeyError as e:
        print(f' ошибка {e}')
        key = None
        return False
