

class AuthError(ValueError):
    def __init__(self, message = 'Вы не авторизованы! Введите код.') -> None:
        super().__init__(message)


class AccountAddingError(ValueError):
    def __init__(self, message = 'Произошла ошибка при добавлении аккаунта.') -> None:
        super().__init__(message)
