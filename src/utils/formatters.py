

def format_work_accounts_to_alias_list(work_accounts):
    output = ""
    for i, work_account in enumerate(work_accounts, start=1):
        # Проверяем, что у пользователя есть alias
        if 'alias' in work_account:
            output += f"{i}. {work_account['alias']}\n"
    return output