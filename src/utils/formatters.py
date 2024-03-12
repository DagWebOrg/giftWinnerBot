

def format_work_accounts_to_alias_list(work_accounts):
    output = ""
    for i, work_account in enumerate(work_accounts, start=1):
        # Проверяем, что у пользователя есть alias
        if 'alias' in work_account:
            output += f"{i}. {work_account['alias']}\n"
    return output


def format_tracking_accounts_to_list(data):
    result = ""
    for i, item in enumerate(data, start=1):
        # Форматируем дату и время в читаемый формат
        formatted_date = item['last_scan_data'].strftime('%Y-%m-%d %H:%M:%S')
        result += f"{i}. Account ID: {item['account_id']}, Alias: {item['alias']}, Last scan data: {formatted_date}\n"
    return result