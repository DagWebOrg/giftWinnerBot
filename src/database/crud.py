from .models import BotUser, TrackingAccount, WorkAccount, GiftPost, ServiceToken
from .tools import DatabaseManager
from utils.exceptions import AccountAddingError


class CRUD():
    @staticmethod
    def get_users():
        with DatabaseManager() as session:
            try:
                users = session.query(BotUser).all()
                session.expunge_all()
                users = [item.id for item in users]
                return users
            except Exception as e:
                raise ValueError(f'Ошибка БД при получении списка пользователей, которым разрешено пользоваться ботом.\n{e}')
    
    @staticmethod
    def create_user(id):
        with DatabaseManager() as session:
            try:
                new_bot_user = BotUser(id = id)
                session.add(new_bot_user)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД при пользователя бота в список разрешенных.\n\n{e}')

    @staticmethod
    def get_work_accounts():
        with DatabaseManager() as session:
            try:
                work_accounts = session.query(WorkAccount).all()
                session.expunge_all()
                work_accounts = [{'alias': item.alias,
                                'login': item.login,
                                'password': item.password,
                                'account_id': item.account_id}
                                  for item in work_accounts]
                return work_accounts
            except Exception as e:
                raise ValueError(f'Ошибка БД при получении списка аккаунтов.\n\n\n{e}')

    @staticmethod
    def create_work_account(alias: str, login: str, password: str, account_id: str):
        with DatabaseManager() as session:
            try:
                new_work_account = WorkAccount(
                    alias = alias,
                    login = login,
                    password = password,
                    account_id = account_id
                )
                session.add(new_work_account)
                session.commit()
            except Exception as e:
                raise AccountAddingError(f'Ошибка БД при добавлении нового аккаунта.\nВозможно такой аккаунт уже существует.\n\n{e}')

    @staticmethod
    def delete_work_account(alias: str):
        with DatabaseManager() as session:
            try:
                work_account = session.query(WorkAccount).filter(WorkAccount.alias == alias).one()
                session.delete(work_account)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД при удалении аккаунта.\n\n{e}')

    @staticmethod
    def get_service_token():
        with DatabaseManager() as session:
            try:
                service_token = session.query(ServiceToken)\
                    .filter(ServiceToken.id == 1).one()
                session.expunge_all()
                return service_token.token
            except Exception as e:
                raise ValueError(f'Ошибка БД при получении токена. Возможно, он не был добавлен: \n\n\n{e}')

    @staticmethod
    def update_service_token(token: str):
        with DatabaseManager() as session:
            try:
                # Указываем id=1, чтобы в случае, когда токен уже существует,
                # он перезаписывался
                new_service_token = ServiceToken(id=1, token=token)
                session.merge(new_service_token)
            except Exception as e:
                raise AccountAddingError(f'Ошибка при обновлении токена.\n\n{e}')

    @staticmethod
    def get_tracking_accounts():
        with DatabaseManager() as session:
            try:
                tracking_accounts = session.query(TrackingAccount).all()
                session.expunge_all()
                tracking_accounts = [{'account_id': item.account_id,
                                'alias': item.alias,
                                'last_scan_data': item.last_scan_data}
                                  for item in tracking_accounts]
                return tracking_accounts
            except Exception as e:
                raise ValueError(f'Ошибка БД при получении списка аккаунтов.\n\n\n{e}')

    @staticmethod
    def create_tracking_account(account_id: str, alias: str):
        with DatabaseManager() as session:
            try:
                new_tracking_account = TrackingAccount(
                    account_id = account_id,
                    alias = alias,
                )
                session.add(new_tracking_account)
                session.commit()
            except Exception as e:
                raise AccountAddingError(f'Ошибка БД при добавлении нового аккаунта.\nВозможно такой аккаунт уже существует.\n\n{e}')

    @staticmethod
    def delete_tracking_account(alias: str):
        with DatabaseManager() as session:
            try:
                tracking_account = session.query(TrackingAccount).filter(TrackingAccount.alias == alias).one()
                session.delete(tracking_account)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД при удалении аккаунта.\n\n{e}')

    @staticmethod
    def create_posts(posts: list):
        with DatabaseManager() as session:
            try:
                for post in posts:
                    # Если добавляемый пост уже существует.
                    existing_post = session.query(GiftPost).filter_by(post_id=post['post_id']).first()
                    if existing_post:
                        # Обновление существующей записи.
                        existing_post.content = post['content']
                    else:
                        # Вставка новой записи.
                        new_post = GiftPost(
                            post_id=post['post_id'],
                            content=post['content']
                        )
                        session.add(new_post)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД при добавлении нового поста.\n\n{e}')

    @staticmethod
    def get_posts():
        with DatabaseManager() as session:
            try:
                posts = session.query(GiftPost).all()
                session.expunge_all()
                posts = [{'post_id': item.post_id,
                        'content': item.content
                         } for item in posts]
                return posts
            except Exception as e:
                raise ValueError(f'Ошибка БД при получении списка постов.\n\n\n{e}')

    @staticmethod
    def delete_post(post_id: str):
        with DatabaseManager() as session:
            try:
                post = session.query(GiftPost).filter(GiftPost.post_id == post_id).one()
                session.delete(post)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД при удалении поста.\n\n{e}')
            
    @staticmethod
    def delete_all_posts():
        with DatabaseManager() as session:
            try:
                posts = session.query(GiftPost).all()
                for post in posts:
                    session.delete(post)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД при удалении постов.\n\n{e}')
