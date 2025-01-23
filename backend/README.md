# Atlas Backend

Atlas Backend is a FastAPI-based service designed to manage and interact with entities and relationships within a Neo4j graph database. This project provides a RESTful API for creating, retrieving, updating, and deleting various entities such as Fields, Industries, Persons, Tables, Teams, and Semantic Blocks, as well as establishing relationships between them.

## Table of Contents

- [Atlas Backend](#atlas-backend)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Environment Variables](#2-environment-variables)
    - [3. Docker Setup](#3-docker-setup)
      - [3.1. Build the Docker Image](#31-build-the-docker-image)
      - [3.2. Run the Neo4j Container](#32-run-the-neo4j-container)
      - [3.3. Run the Backend Container](#33-run-the-backend-container)
    - [4. Alternatively, Using Docker Compose](#4-alternatively-using-docker-compose)
  - [Running the Project](#running-the-project)
    - [Using Docker](#using-docker)
    - [Using Docker Compose](#using-docker-compose)
  - [API Documentation](#api-documentation)
    - [Entities Endpoints](#entities-endpoints)
      - [Fields](#fields)
      - [Industries](#industries)
      - [Persons](#persons)
      - [Tables](#tables)
      - [Teams](#teams)
      - [Semantic Blocks](#semantic-blocks)
    - [Relationships Endpoints](#relationships-endpoints)
      - [Add Field to Table](#add-field-to-table)
      - [Table Source Of Table](#table-source-of-table)
      - [Table Belongs To Industry](#table-belongs-to-industry)
      - [Table Maintained By Team](#table-maintained-by-team)
      - [Table Has Responsible](#table-has-responsible)
      - [Table Part Of Semantic Block](#table-part-of-semantic-block)
      - [Person Belongs To Team](#person-belongs-to-team)
      - [Field References Field](#field-references-field)
    - [Drafts Endpoints](#drafts-endpoints)
      - [Create Draft](#create-draft)
      - [Get Drafts](#get-drafts)
      - [Delete Draft](#delete-draft)
  - [Examples](#examples)
    - [Creating a Person](#creating-a-person)
    - [Creating a Table](#creating-a-table)
    - [Establishing a Relationship](#establishing-a-relationship)
  - [Testing](#testing)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **Entity Management**: CRUD operations for Fields, Industries, Persons, Tables, Teams, and Semantic Blocks.
- **Relationship Management**: Establish and manage relationships like `HAS_FIELD`, `SOURCE_OF`, `BELONGS_TO`, `MAINTAINED_BY`, etc., between entities.
- **Draft Management**: Manage drafts related to Tables, including responsible persons and sources.
- **Graph Database Integration**: Utilizes Neo4j for efficient graph-based data storage and querying.
- **Dockerized Setup**: Simplifies deployment and environment management using Docker.
- **API Documentation**: Interactive documentation available via Swagger UI and ReDoc.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) (optional, if using Docker Compose).
- Alternatively, Python 3.11 and related dependencies if running without Docker.

## Installation

### 1. Clone the Repository

```bash
git clone <repository_url>
cd atlas/backend
```

### 2. Environment Variables

Create a `.env` file in the `atlas/backend` directory based on the provided `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file to configure the environment as needed:

```env
ENV=dev

NEO4J_PASSWORD=password
NEO4J_HOST=neo4j
NEO4J_PORT=7687
```

> **Note**: Replace `password` with a strong password of your choice.

### 3. Docker Setup

Ensure Docker is installed and running on your machine.

#### 3.1. Build the Docker Image

```bash
docker build -t atlas-backend .
```

#### 3.2. Run the Neo4j Container

If you don't already have a Neo4j instance running, you can start one using Docker:

```bash
docker run -d \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    neo4j:5.10.0
```

> **Note**: Replace `password` with the password you set in your `.env` file.

#### 3.3. Run the Backend Container

```bash
docker run -d \
    --name atlas-backend \
    -p 8073:8073 \
    --env-file .env \
    --link neo4j:neo4j \
    atlas-backend
```

> **Note**: This command maps port `8073` of the backend container to port `8073` on your host machine.

### 4. Alternatively, Using Docker Compose

If you prefer using Docker Compose, create a `docker-compose.yml` file in the `atlas/backend` directory:

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.10.0
    container_name: neo4j
    environment:
      NEO4J_AUTH: neo4j/password
    ports:
      - "7474:7474"
      - "7687:7687"

  backend:
    build: .
    container_name: atlas-backend
    environment:
      - ENV=dev
      - NEO4J_HOST=neo4j
      - NEO4J_PORT=7687
      - NEO4J_PASSWORD=password
    ports:
      - "8073:8073"
    depends_on:
      - neo4j
```

> **Note**: Replace `password` with the password you set in your `.env` file.

Start both services:

```bash
docker-compose up -d
```

## Running the Project

After building the Docker image and ensuring Neo4j is running, start the backend service.

### Using Docker

```bash
docker start atlas-backend
```

### Using Docker Compose

```bash
docker-compose up -d
```

The FastAPI application will be accessible at `http://localhost:8073`.

## API Documentation

FastAPI provides interactive API documentation available at:

- **Swagger UI**: [http://localhost:8073/docs](http://localhost:8073/docs)
- **ReDoc**: [http://localhost:8073/redoc](http://localhost:8073/redoc)

### Entities Endpoints

#### Fields

- **Create Field**
  - **Endpoint**: `POST /api/entities/fields/`
  - **Body**:
    ```json
    {
      "name": "Field Name",
      "description": "Field Description"
    }
    ```
- **Get All Fields**
  - **Endpoint**: `GET /api/entities/fields/`
- **Get Field by ID**
  - **Endpoint**: `GET /api/entities/fields/{field_id}`
- **Update Field**
  - **Endpoint**: `PUT /api/entities/fields/{field_id}`
  - **Body**:
    ```json
    {
      "name": "Updated Field Name",
      "description": "Updated Description"
    }
    ```
- **Delete Field**
  - **Endpoint**: `DELETE /api/entities/fields/{field_id}`

#### Industries

- **Create Industry**
  - **Endpoint**: `POST /api/entities/industries/`
  - **Body**:
    ```json
    {
      "id": "GR",
      "name": "Golden Record"
    }
    ```
- **Get All Industries**
  - **Endpoint**: `GET /api/entities/industries/`
- **Get Industry by ID**
  - **Endpoint**: `GET /api/entities/industries/{industry_id}`
- **Update Industry**
  - **Endpoint**: `PUT /api/entities/industries/{industry_id}`
  - **Body**:
    ```json
    {
      "id": "GR",
      "name": "Updated Industry Name"
    }
    ```
- **Delete Industry**
  - **Endpoint**: `DELETE /api/entities/industries/{industry_id}`

#### Persons

- **Create Person**
  - **Endpoint**: `POST /api/entities/persons/`
  - **Body**:
    ```json
    {
      "first_name": "Alan",
      "last_name": "Rickman",
      "email": "alan.rickman@mts.ru"
    }
    ```
- **Get All Persons**
  - **Endpoint**: `GET /api/entities/persons/`
- **Get Person by Email**
  - **Endpoint**: `GET /api/entities/persons/{email}`
- **Update Person**
  - **Endpoint**: `PUT /api/entities/persons/{email}`
  - **Body**:
    ```json
    {
      "first_name": "Alan",
      "last_name": "Rickman",
      "email": "alan.rickman@mts.ru"
    }
    ```
- **Delete Person**
  - **Endpoint**: `DELETE /api/entities/persons/{email}`

#### Tables

- **Create Table**
  - **Endpoint**: `POST /api/entities/tables/`
  - **Body**:
    ```json
    {
      "name": "Employees",
      "description": "Employee Details"
    }
    ```
- **Get All Tables**
  - **Endpoint**: `GET /api/entities/tables/`
- **Get Table by Name**
  - **Endpoint**: `GET /api/entities/tables/{table_name}`
- **Update Table**
  - **Endpoint**: `PUT /api/entities/tables/{table_name}`
  - **Body**:
    ```json
    {
      "name": "Employees",
      "description": "Updated Description"
    }
    ```
- **Delete Table**
  - **Endpoint**: `DELETE /api/entities/tables/{table_name}`

#### Teams

- **Create Team**
  - **Endpoint**: `POST /api/entities/teams/`
  - **Body**:
    ```json
    {
      "id": "PML",
      "name": "Person Modeling Lab"
    }
    ```
- **Get All Teams**
  - **Endpoint**: `GET /api/entities/teams/`
- **Get Team by ID**
  - **Endpoint**: `GET /api/entities/teams/{team_id}`
- **Update Team**
  - **Endpoint**: `PUT /api/entities/teams/{team_id}`
  - **Body**:
    ```json
    {
      "id": "PML",
      "name": "Updated Team Name"
    }
    ```
- **Delete Team**
  - **Endpoint**: `DELETE /api/entities/teams/{team_id}`

#### Semantic Blocks

- **Create Semantic Block**
  - **Endpoint**: `POST /api/entities/semantic-blocks/`
  - **Body**:
    ```json
    {
      "id": "SB1",
      "title": "Block Title",
      "content": "Block Content"
    }
    ```
- **Get All Semantic Blocks**
  - **Endpoint**: `GET /api/entities/semantic-blocks/`
- **Get Semantic Block by ID**
  - **Endpoint**: `GET /api/entities/semantic-blocks/{block_id}`
- **Update Semantic Block**
  - **Endpoint**: `PUT /api/entities/semantic-blocks/{block_id}`
  - **Body**:
    ```json
    {
      "id": "SB1",
      "title": "Updated Title",
      "content": "Updated Content"
    }
    ```
- **Delete Semantic Block**
  - **Endpoint**: `DELETE /api/entities/semantic-blocks/{block_id}`

### Relationships Endpoints

#### Add Field to Table

- **Endpoint**: `POST /api/relationships/table/add_field`
- **Body**:
  ```json
  {
    "table_name": "Employees",
    "field_id": "field-uuid-1234"
  }
  ```

#### Table Source Of Table

- **Endpoint**: `POST /api/relationships/table/source_of`
- **Body**:
  ```json
  {
    "source_name": "Employees",
    "target_name": "Departments"
  }
  ```

#### Table Belongs To Industry

- **Endpoint**: `POST /api/relationships/table/belongs_to`
- **Body**:
  ```json
  {
    "table_name": "Employees",
    "industry_id": "GR"
  }
  ```

#### Table Maintained By Team

- **Endpoint**: `POST /api/relationships/table/maintained_by`
- **Body**:
  ```json
  {
    "table_name": "Employees",
    "team_id": "PML"
  }
  ```

#### Table Has Responsible

- **Endpoint**: `POST /api/relationships/table/has_responsible`
- **Body**:
  ```json
  {
    "table_name": "Employees",
    "person_email": "alan.rickman@mts.ru"
  }
  ```

#### Table Part Of Semantic Block

- **Endpoint**: `POST /api/relationships/table/part_of`
- **Body**:
  ```json
  {
    "table_name": "Employees",
    "block_id": "SB1"
  }
  ```

#### Person Belongs To Team

- **Endpoint**: `POST /api/relationships/person/belongs_to`
- **Body**:
  ```json
  {
    "email": "alan.rickman@mts.ru",
    "team_id": "PML"
  }
  ```

#### Field References Field

- **Endpoint**: `POST /api/relationships/field/references`
- **Body**:
  ```json
  {
    "field_id": "field-uuid-1234",
    "ref_field_id": "field-uuid-5678"
  }
  ```

### Drafts Endpoints

#### Create Draft

- **Endpoint**: `POST /api/drafts/`
- **Body**:
  ```json
  {
    "name": "Draft Table",
    "industry": "GR",
    "description": "Description of the draft table",
    "team": "PML",
    "responsible_person": "alan.rickman@mts.ru",
    "sources_tables": ["SourceTable1", "SourceTable2"],
    "fields": [
      {
        "name": "Field1",
        "description": "Description1"
      },
      {
        "name": "Field2",
        "description": "Description2"
      }
    ]
  }
  ```

#### Get Drafts

- **Endpoint**: `GET /api/drafts/?email=alan.rickman@mts.ru`

#### Delete Draft

- **Endpoint**: `DELETE /api/drafts/?email=alan.rickman@mts.ru&table_name=Draft Table`

## Examples

### Creating a Person

**Request:**

```http
POST /api/entities/persons/
Content-Type: application/json

{
  "first_name": "Harry",
  "last_name": "Potter",
  "email": "harry.potter@hogwarts.edu"
}
```

**Response:**

```json
{
  "first_name": "Harry",
  "last_name": "Potter",
  "email": "harry.potter@hogwarts.edu"
}
```

### Creating a Table

**Request:**

```http
POST /api/entities/tables/
Content-Type: application/json

{
  "name": "Employees",
  "description": "Employee Details"
}
```

**Response:**

```json
{
  "name": "Employees",
  "description": "Employee Details"
}
```

### Establishing a Relationship

**Creating a `BELONGS_TO` relationship between a Table and an Industry**

**Request:**

```http
POST /api/relationships/table/belongs_to
Content-Type: application/json

{
  "table_name": "Employees",
  "industry_id": "GR"
}
```

**Response:**

```json
{
  "detail": "Связь (Table)-[:BELONGS_TO]->(Industry) создана"
}
```

## Testing

The project uses `pytest` for testing. To run the tests:

1. **Install Development Dependencies**:

   ```bash
   pip install -r requirements/dev.txt
   ```

2. **Run Tests**:

   ```bash
   pytest
   ```

> **Note**: Ensure that the Neo4j instance is running before executing tests.

## Project Structure

```
atlas/
└── backend/
    ├── .env.example
    ├── Dockerfile
    ├── main.py
    ├── requirements/
    │   ├── codestyle.txt
    │   ├── dev.txt
    │   └── prod.txt
    ├── core/
    │   └── config.py
    ├── db/
    │   ├── init_db.py
    │   └── neo4j_client.py
    ├── routers/
    │   ├── __init__.py
    │   ├── entitis/
    │   │   ├── __init__.py
    │   │   ├── drafts.py
    │   │   ├── field.py
    │   │   ├── industry.py
    │   │   ├── persons.py
    │   │   ├── semantic_block.py
    │   │   ├── table.py
    │   │   └── team.py
    │   ├── relationships/
    │   │   ├── __init__.py
    │   │   └── relationships.py
    │   └── drafts/
    │       ├── __init__.py
    │       └── drafts.py
    └── schemas/
        ├── draft.py
        ├── field.py
        ├── industry.py
        ├── person.py
        ├── relationships.py
        ├── semantic_block.py
        ├── table.py
        └── team.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note**: Ensure that all dependencies and configurations are properly set up as per the instructions. If you encounter any issues, feel free to open an issue in the repository.
