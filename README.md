# FastAPI-Clean-Mongo

base Fastapi project with mongodb as the database for RestAPI applications
![image of docs](https://github.com/movassaghi6/fastapi-clean-mongo/blob/main/docs.png)

## Table of Contents

- [Features](##Features)
- [Installation](https://www.notion.so/re-b39773b9a6994ba08627024ac12c20b0?pvs=21)
- [Usage](https://www.notion.so/re-b39773b9a6994ba08627024ac12c20b0?pvs=21)
- [Project Structure](https://www.notion.so/re-b39773b9a6994ba08627024ac12c20b0?pvs=21)
- [Contributing](https://www.notion.so/re-b39773b9a6994ba08627024ac12c20b0?pvs=21)
- [License](https://www.notion.so/re-b39773b9a6994ba08627024ac12c20b0?pvs=21)

## Features

- 🚀 **FastAPI** for high-performance web APIs
- 📦 **MongoDB** for flexible, scalable data storage
- 🎯 **Clean Architecture** ensuring modular and maintainable code
- 🛠️ **Poetry** for easy dependency management and packaging

## Installation

### Prerequisites

- Python 3.12
- FastAPI
- MongoDB
- Pydantic
- Pymongo
- Poetry

### Steps

1. **Clone the repository**:
    
    ```
    
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    
    ```
    
2. **Install dependencies**:
    
    ```
    
    poetry install
    
    ```
    
3. **Run the application**:
    
    ```
    
    poetry run uvicorn api.main:app --reload
    
    ```
    

### 

### Description
Clean Architecture, proposed by Robert C. Martin (Uncle Bob), aims to separate the concerns of an application into distinct layers. This helps in creating a system that is both flexible and maintainable. Here's a breakdown of how the folders you mentioned typically relate to the layers in Clean Architecture:

- **API**: Interface Adapters (Delivery Mechanism)
- **Core**: Application Business Rules (Use Cases) and Enterprise Business Rules (Entities)
- **Model**: Data Layer
- **Repository**: Interface Adapters (Data Access)
- **Schema**: Interface Adapters (Data Transfer Objects or Validation Schemas)

This structure maintains a clean separation of concerns:

- **API** handles external communication.
- **Core** defines the core business logic and rules.
- **Model** represents the database structure.
- **Repository** manages data access and manipulation.
- **Schema** defines the data formats for communication with the database.

### ToDo:

complete Tests

implement Authentication

logging system

cache system
