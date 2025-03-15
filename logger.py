import logging
import os
from logging.handlers import RotatingFileHandler

# 📌 Название лог-файла
LOG_FILE = "logs/test_log.log"

# 📌 Создаём директорию для логов, если её нет
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 📌 Создаём логгер
logger = logging.getLogger("QA_Automation_Logger")
logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования

# ✅ Формат логирования
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 📌 Логирование в файл (с ротацией)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# 📌 Логирование в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # В консоли можно видеть DEBUG
console_handler.setFormatter(formatter)

# ✅ Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 📌 Выключаем дублирование логов от библиотеки `selenium` и `urllib3`
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# ✅ Логгер готов
logger.info("Logger initialized successfully!")
