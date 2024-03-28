import subprocess
from dotenv import load_dotenv
import os

# Загрузка данных из файла .env
load_dotenv()

# Чтение токена из файла .env
token = os.getenv("TOKEN")

# Открытие файла log_err.txt в режиме записи
log_file = open("log_err.txt", "w", encoding="utf-8")

try:
    import vk_api
    import random
    import time
    import json
    import configparser
    import os

    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    print("\n -----------------------------\n")
    time.sleep(0.45)

    # Авторизация в VK API
    print(" authorization...")
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    time.sleep(0.45)

    # Проверка на валидность
    print(" reading validity...\n")
    def check_token_validity():
        try:
            vk.users.get()
            return True
        except vk_api.exceptions.ApiError as e:
            with open('log_err.txt', 'a', encoding="utf-8") as log_file:
                log_file.write(str(e) + '\n')
            return False

    print(" reading data...")
    config = configparser.ConfigParser()
    config.read('config.ini', encoding="utf-8")
    words = config['DATA']['words'].split('*')

    time.sleep(0.15)

    print("\n -----------------------------\n")
    time.sleep(1.75)

    clear_console()

    def update_online_status():
        vk.account.setOnline()

    def update_status_with_random_word():
        random_word = random.choice(words)
        vk.status.set(text=random_word)

    # Основной цикл программы
    while True:
        current_time = time.strftime("%H:%M", time.localtime())
        if not check_token_validity():
            print(" error: 0x703\n")
            new_token = input(" enter new token: ")
            os.environ["TOKEN"] = new_token  # Обновляем переменную среды с новым токеном

            with open('.env', 'w') as f:
                f.write(f"TOKEN={new_token}\n")  # Записываем новый токен в файл .env

            vk_session = vk_api.VkApi(token=new_token)
            vk = vk_session.get_api()
            print("\n token update...\n")
            time.sleep(1)
            clear_console()
            subprocess.call(['python', 'main.py'])

        # Пауза в 5 минут
        time.sleep(300)

except Exception as e:
    # Запись ошибки в файл log_err.txt
    log_file.write(str(e))
    log_file.write("\n")

finally:
    # Закрытие файла log_err.txt
    log_file.close()
