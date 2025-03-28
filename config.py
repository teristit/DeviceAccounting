import os

# Теперь для SQLite:  Путь к файлу базы данных
# Можно использовать относительный путь (относительно   или где вы запускаете)
# или абсолютный путь
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./device_accounting.db") # Относительный путь (рекомендуется)
#DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///C:/path/to/your/device_accounting.db") # Абсолютный путь (для примера)
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")