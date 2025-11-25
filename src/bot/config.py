import os
from dotenv import load_dotenv
from typing import Optional

# Загружаем переменные окружения
load_dotenv()

class Settings:
    
    # VK
    VK_BOT_TOKEN: str = os.getenv("VK_BOT_TOKEN", "")
    VK_GROUP_ID: int = int(os.getenv("VK_GROUP_ID", "0"))

    # App
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    
    def validate(self) -> bool:
        """Проверяет обязательные настройки"""
        errors = []
        
        if not self.VK_BOT_TOKEN:
            errors.append("VK_BOT_TOKEN не установлен")
        
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