from langchain_core.prompts import PromptTemplate

research_prompt = PromptTemplate(
    template="""
Ты агент-исследователь данных.
Ты специализаруешься на том, чтобы достать нужную информацию из текста для описания таблицы.
Ты используешь доступные инструменты для поиска информации в Confluence.

Таблица для которой нужно найти информацию: {table_name}

Пожалуйста, создай JSON с ключами:
- industry: примерная индустрия (определи, если возможно)
- description: краткое описание таблицы (в одном предложении)
- team: команда, отвечающая за таблицу (если есть)
- responsible_person: почта отвественного за таблицу (если есть, вида example@mts.ru)
- fields: список объектов вида {{name: str, description: str}} для столбцов таблицы

Если модель не смогла создать ответ для какого-то поля, верни Null для него.

Проанализируй следующий текст:
{description}

Верни только итоговый JSON без каких либо дополнений.
""",
    input_variables=["table_name", "description"],
)


unify_prompt = PromptTemplate(
    template="""
Ты специализируешься на объединении информации из разных источников в виде json в один json файл.

Таблица для которой нужно объединить: {table_name}

Пожалуйста, дополни JSON из confluence с помощью JSON из gitlab. Приоритет отдавай описанию из confluence.

Правила:
1. Если модель не смогла создать ответ для какого-то поля, верни Null для него.
2. Старайся писать на русском языке, если это не касается названий команд и индустрий.
3. Не дублируй поля в JSON. Это же касается полей самой таблицы в поле fields.

JSON из Confluence:
{confluence_json}

JSON из Gitlab:
{gitlab_json}
""",
    input_variables=["table_name", "confluence_json", "gitlab_json"],
)


relation_prompt = PromptTemplate(
    template="""
Ты специализируешься на поиске связей между таблицами.

Найди в коде таблицы, которые используются для создания таблицы с названием {table_name}.
Найди названия (схему или путь до этих таблиц).

Вот код из Gitlab:
{gitlan_code}

В ответ ты должен вернуть ТОЛЬКО JSON вида:
{{"sources_tables": List[str]}}
""",
    input_variables=["table_name"],
)


teams_refiner = PromptTemplate(
    template="""
Ты уточняешь по навзанию команды ее ID в системе.
Найди наиоболее подходящую команду по названию и верни ее ID.

Если такой команды не найдено, то верни Null.

Список всех команд:
{teams}

Команда для которой нужно найти подходящий ID: {team_name}.

В ответ ты должен вернуть ТОЛЬКО JSON вида:
{{"team": ```ID который ты выбрал```}}
""",
    input_variables=["teams", "team_name"],
)
