# ATLAS — Guide for Data Voyagers

## Описание проекта

Atlas - это комплексная система для управления знаниями о данных, состоящая из нескольких взаимосвязанных сервисов. Система помогает организациям эффективно управлять метаданными, документировать источники данных и предоставлять удобный интерфейс для работы с информацией о данных.

## Основные компоненты

```mermaid
graph TB
    User((Пользователь)) --> Frontend[Atlas Frontend]
    Frontend --> Backend[Atlas Backend]
    Frontend --> Agents[Atlas Agents]

    subgraph Sources Examples
        Confluence[(Confluence Docs)]
        GitLab[(GitLab ETL)]
        Schema[(Schema Info)]
    end

    Agents --> Backend
    Agents --> Sources
    Backend --> Neo4j[(Neo4j Graph DB)]

    style Frontend fill:#f9d,stroke:#333
    style Backend fill:#9df,stroke:#333
    style Agents fill:#df9,stroke:#333
    style Neo4j fill:#fd9,stroke:#333
```

### 1. Atlas Agents

Сервис интеллектуальных агентов, включающий два специализированных агента:

- **Exploration Agent** - исследует и собирает информацию о таблицах:
  - Анализирует схемы баз данных
  - Извлекает информацию из GitLab и Confluence
  - Создает структурированные описания таблиц
  - Определяет связи между таблицами
  - Уточняет информацию о командах

- **Exploitation Agent** - отвечает на вопросы пользователей:
  - Обрабатывает естественно-языковые запросы
  - Использует GigaChat для генерации ответов
  - Работает с графовой базой данных Neo4j

Схема агентов:
```mermaid
graph TB
    subgraph "Exploration Agent"
        EA[Exploration Agent]
        RP[Research Prompts]
        UP[Unify Prompts]
        TP[Team Refiner Prompts]
        RFP[Relation Finder Prompts]

        EA --> RP
        EA --> UP
        EA --> TP
        EA --> RFP

        RP --> GC1[GigaChat]
        UP --> GC2[GigaChat]
        TP --> GC3[GigaChat]
        RFP --> GC4[GigaChat]
    end

    subgraph "Exploitation Agent"
        QA[QA Agent]
        QAP[QA Prompts]

        QA --> QAP
        QAP --> GC5[GigaChat]
    end

    Sources[(Sources Examples)] --> EA
    EA --> Neo4j[(Neo4j)]
    QA --> Neo4j
    User((Пользователь)) --> QA

    style EA fill:#90EE90,stroke:#333
    style QA fill:#FFB6C1,stroke:#333
```

### 2. Atlas Backend

REST API сервис для работы с графовой базой данных Neo4j:

- Управление сущностями (таблицы, поля, команды, индустрии и др.)
- Управление связями между сущностями
- Работа с черновиками описаний таблиц
- Аутентификация пользователей

Схема данных:
```mermaid
erDiagram
    Table {
        string name PK
        string description
    }
    Field {
        string id PK
        string name
        string description
    }
    Industry {
        string id PK
        string name
    }
    Team {
        string id PK
        string name
    }
    Person {
        string email PK
        string first_name
        string last_name
    }
    SemanticBlock {
        string id PK
        string title
        string content
    }

    Table ||--o{ Field : HAS_FIELD
    Table ||--o{ Table : SOURCE_OF
    Table ||--o{ Industry : BELONGS_TO
    Table ||--o{ Team : MAINTAINED_BY
    Table ||--o{ Person : HAS_RESPONSIBLE
    Table ||--o{ SemanticBlock : PART_OF
    Person ||--o{ Team : BELONGS_TO
    Field ||--o{ Field : REFERENCES
```

### 3. Atlas Frontend

Web-интерфейс для взаимодействия с системой:

- Просмотр и подтверждение черновиков
- Чат с Exploitation Agent для получения информации
- Визуализация графа знаний
- Простая email-аутентификация

### 4. Sources Examples

Мокап-сервис для демонстрации работы с источниками данных:

- Эмуляция Confluence с документацией
- Эмуляция GitLab с ETL-скриптами
- API для поиска информации по таблицам

## Запуск проекта

### Предварительные требования

- Docker и Docker Compose
- Git для клонирования репозитория

### Шаги по запуску

1. Клонировать репозиторий:
```bash
git clone <repository-url>
cd atlas
```

2. Создать и настроить файлы окружения:

```bash
# agents/.env
GIGA_KEY=ваш_ключ_gigachat
NEO4J_PASSWORD=ваш_пароль

# backend/.env
NEO4J_PASSWORD=ваш_пароль
NEO4J_HOST=neo4j
NEO4J_PORT=7687
```

3. Запустить все сервисы через Docker Compose:

```bash
docker-compose up -d
```

После запуска будут доступны следующие сервисы:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8073
- Agents API: http://localhost:8053
- Sources Examples API: http://localhost:8043
- Neo4j Browser: http://localhost:7474

## Основные функции

### Исследование данных

1. Agents сервис автоматически исследует новые таблицы:
```bash
curl -X POST http://localhost:8053/create_drafts
```

2. Созданные черновики появляются в веб-интерфейсе
3. Пользователь просматривает и подтверждает черновики
4. После подтверждения информация сохраняется в графовой базе данных

### Получение информации

1. Пользователь задает вопрос через веб-интерфейс
2. Exploitation Agent обрабатывает вопрос и генерирует ответ на основе данных из Neo4j
3. Пользователь получает структурированный ответ

## Особенности системы

- **Автоматизация**: Автоматический сбор и структурирование информации о данных
- **Интеллектуальная обработка**: Использование LLM для понимания контекста и генерации ответов
- **Графовая база данных**: Эффективное хранение связей между сущностями
- **Современный стек**: React, FastAPI, Neo4j, Docker
- **Масштабируемость**: Микросервисная архитектура позволяет легко масштабировать систему

## Рекомендации по разработке

- Используйте pre-commit hooks для поддержания качества кода
- Следуйте структуре проекта при добавлении новых компонентов
- Документируйте изменения в API и новые функции
- Используйте типизацию в Python и TypeScript
