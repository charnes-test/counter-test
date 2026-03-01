# Используем легкую версию Python (Best Practice: экономия места)
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Сначала копируем только requirements (Best Practice: кэширование слоев)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальной код
COPY . .

# Указываем команду запуска
CMD ["python", "main.py"]
