# FastAPI-Clean-Mongo

base Fastapi project with mongodb as the database for RestAPI applications

![Screenshot of API endpoint](https://github.com/movassaghi6/fastapi-clean-mongo/blob/main/docs.png)

## Table of Contents

- [Features](#Features)
- [Installation](#Installation)
- [Description](#Description)
- [ToDo](#ToDo)



## Features

- 🚀 **FastAPI** for high-performance web APIs
- 📦 **MongoDB** for flexible, scalable data storage
- 🎯 **Clean Architecture** ensuring modular and maintainable code
- 🛠️ **Poetry** for easy dependency management and packaging

## Installation

### Installation using poetry

#### Prerequisites

- Python 3.12
- FastAPI
- MongoDB
- Pydantic
- Pymongo
- Poetry

#### Steps

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

### Installation using docker

#### Prerequisites
- Docker
- Docker Compose

#### Steps

1. **Clone the repository**:

    ```
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Build and run the Docker containers using Docker Compose**:

    ```
    docker-compose up --build
    ```

This command will:
- Build the Docker image for your FastAPI application.
- Start the FastAPI application in a container.
- Start MongoDB in another container.

3. **Access the application**:

    Open your web browser and go to `http://localhost:8000`.
    

## Description

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

## ToDo:

- [] complete Tests

- [x] implement Authentication

- [ ] logging system

- [ ] cache system
