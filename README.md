Qase AI Test Case Generator (Hybrid Mode)

Инструмент для QA, который:
1.	Читает проектную документацию из разных файлов
2.  Помогает сгенерировать тест-кейсы через ИИ (ChatGPT)
3.  Фвтоматически конвертирует их в CSV для импорта в Qase

⚠️ Не требует API ключа — работает в гибридном режиме (через ChatGPT вручную)
```mermaid
flowchart TD
    A[Документация<br/>data/input] --> B[python -m app.main]
    B --> C[prompt_for_chatgpt.txt]
    C --> D[ChatGPT]
    D --> E[manual_response.json]
    E --> F[python -m app.main]
    F --> G[qase_import.csv]
    G --> H[Импорт в Qase]

🔧 Требования
1. MacOS / Linux / Windows
2. Python 3.10+
3. PyCharm (или любой IDE)

🚀 Установка

1. git clone <repo>
cd qase_ai_generator
python3 -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt

📂 Структура папок
data/
├── input/        ← документация
├── output/       ← результаты
└── templates/
    └── qase_template.csv ← сюда кладем пример тест-кейса (описано в пункте Подготовка Qase)

📥 Подготовка Qase (📌 Важно: не создавай CSV вручную)
1. Зайди в Qase
2. Экспортируй любой тест-кейс
3. Сохрани как: data/templates/qase_template.csv

▶️ Пошаговый процесс
1. Добавь документацию в data/input/
2. Сгенерируй prompt - в терминале введи: python -m app.main 
📦 Результат:
data/output/
├── prompt_for_chatgpt.txt
├── source_preview.txt
3. Используй ChatGPT
    a.Открой prompt_for_chatgpt.txt
    b.Скопируй весь текст
    c.Вставь в ChatGPT
    d.Получи ответ
4. Создай файл data/output/manual_response.json 
5. Вставь в manual_response.json ответ ChatGPT
⚠️ Важно получить формат
{
  "test_cases": [
    {
      "title": "User can log in with valid email and password",
      "priority": "High"
    }
  ]
}
6. Сгенирируй CSV - в терминале введи: python -m app.main
📦 Результат:
data/output/
├── generated_cases.json
├── qase_import.csv
7. Импорт в Qase
    a. Открой Qase
    b. Import → Qase.io CSV
    c. Загрузи qase_import.csv
8. Очистка проекта (Удаляет все файлы из data/output/) - в терминале введи: python -m app.main clean 
