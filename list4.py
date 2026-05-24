# Django автоматически поддерживает многопользовательский режим
# через сессии и независимые соединения с БД

# Каждый пользователь имеет свои данные через связь user
user_report = DatasetOtchet.objects.get(user=request.user)  # Разные user_id

# Настройка сессий (settings.py)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 недели