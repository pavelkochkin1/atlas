# Витрина: Чтение в «Строки»

Витрина: /data/stroki/readings
Программист: Алан Рикмэн(rickman@mts.ru)

Содержит логи сессий чтения:
- user_id
- book_id
- start_time, end_time
- reading_duration (время чтения в секундах)
- total_reading_duration, books_opened_count — агрегаты по пользователю

Возможное назначение: аналитика поведения читателей, популярность книг.

Недостатки:
- Нет связи с полноценным справочником книг
- Часть старых логов потеряна
