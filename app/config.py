from pathlib import Path
import os
import configparser

CONFIG_FILE = Path("config.conf")

def create_default_config():
    """Создает файл конфигурации с настройками по умолчанию, если он отсутствует."""
    if not CONFIG_FILE.exists():
        config = configparser.ConfigParser()
        config["server"] = {
            "secret_key": os.urandom(24).hex(),
            "database_uri": "sqlite:///users.db",
            "host": "0.0.0.0",
            "port": "5000",
            "debug": "true"
        }
        with CONFIG_FILE.open("w") as configfile:
            config.write(configfile)

# Создаем конфиг, если его нет
create_default_config()

class Config:
    """Класс для загрузки конфигурации приложения."""
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    @classmethod
    def load_config(cls):
        """Читает конфигурацию из файла с обработкой ошибок."""
        try:
            cls.HOST = cls.config.get("server", "host", fallback="0.0.0.0")
            cls.PORT = cls.config.getint("server", "port", fallback=5000)
            cls.DEBUG = cls.config.getboolean("server", "debug", fallback=True)
            cls.SECRET_KEY = cls.config.get("server", "secret_key")
            cls.SQLALCHEMY_DATABASE_URI = cls.config.get("server", "database_uri")
            cls.SQLALCHEMY_TRACK_MODIFICATIONS = False
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(f"Ошибка в файле конфигурации: {e}")
            raise SystemExit("Программа завершена из-за ошибки в конфигурации.")

    @classmethod
    def reload(cls):
        """Перезагружает конфигурацию из файла."""
        if not CONFIG_FILE.exists():
            print("Файл конфигурации отсутствует, создаем заново...")
            create_default_config()
        
        cls.config.read(CONFIG_FILE)
        cls.load_config()
        print("Конфигурация перезагружена.")

# Загружаем конфиг при инициализации
Config.load_config()
