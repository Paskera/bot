import os
from dotenv import load_dotenv
from typing import Optional

# Загружаем переменные окружения
load_dotenv()

class Settings:

    # Database
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "vk_bot")
    
    # VK
    VK_BOT_TOKEN: str = os.getenv("VK_BOT_TOKEN", "")
    VK_GROUP_ID: int = int(os.getenv("VK_GROUP_ID", "0"))

    # App
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def database_url(self) -> str:
        """URL для подключения к PostgreSQL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def async_database_url(self) -> str:
        """Асинхронный URL для подключения"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def validate(self) -> bool:
        """Проверяет обязательные настройки"""
        errors = []
        
        if not self.VK_BOT_TOKEN:
            errors.append("VK_BOT_TOKEN не установлен")
        
        if not self.DB_PASSWORD:
            errors.append("DB_PASSWORD не установлен")
        
        if errors:
            raise ValueError("Ошибки конфигурации:\n- " + "\n- ".join(errors))
        
        return True

# Глобальный экземпляр настроек
settings = Settings()

# Валидируем настройки при импорте
try:
    settings.validate()
    print("✅ Конфигурация загружена успешно")
except ValueError as e:
    print(f"❌ Ошибка конфигурации: {e}")
    exit(1)