from vk_api import vk_api

def auth_handler():
    key = int(input("2 auth factor code: "))
    remember_device = True
    return key, remember_device

def auth(login='', password='', token=None):
    if token:
        group = vk_api.VkApi(token=token)
        return group
    elif login and password:
        try:
            me = vk_api.VkApi(\
                            login=login,\
                            password=password,\
                            app_id=6287487,\
                            client_secret="QbYic1K3lEV5kTGiqlq2")
            me.auth()
        except Exception as e:
            me = vk_api.VkApi(login=login, password=password, auth_handler=auth_handler, app_id=6287487, client_secret="QbYic1K3lEV5kTGiqlq2")
            me.auth()
        return me
    else:
        return print('Need pass and login or group token')
    
auth()