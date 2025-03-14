def check_internet_connection():
    import requests
    try:
        # Отправляем запрос к Google с ограничением по времени в 3 секунды
        response = requests.get("http://www.google.com", timeout=3)
        # Если запрос прошёл успешно, возвращаем True
        return response.status_code == 200
    except requests.ConnectionError:
        # Если не удалось подключиться, возвращаем False
        return False

