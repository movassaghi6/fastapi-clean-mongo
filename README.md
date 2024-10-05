# FastAPI-Clean-Mongo

base Fastapi project with mongodb as the database for RestAPI applications

![Screenshot of API endpoint](https://github.com/movassaghi6/fastapi-clean-mongo/blob/main/docs-v2.png)

## Table of Contents

- [Features](#Features)
- [Installation](#Installation)
- [Description](#Description)
- [ToDo](#ToDo)



## Features

- 🚀 **FastAPI** for high-performance web APIs
- 📦 **MongoDB** for flexible, scalable data storage
- 🎯 **Clean Architecture** ensuring modular and maintainable code
- 🔐 **OAuth2.0 JWT Authentication** for secure user authentication
- 📖 **Well-Documented** Comprehensive documentation is provided for all modules and functions
- 🛠️ **Poetry** for easy dependency management and packaging

## Installation

### Environment Variables Guide

To run the application, you need to set up a `.env` file in the root directory of the project. Below is a description of each environment variable that should be included:

#### Security Configuration

- **`SECRET_KEY`**: 
  - Description: A secret key used for encoding and decoding JWT tokens. Make sure to set this to a strong, random string to enhance security.
  - Example: `SECRET_KEY="your_secret_key"`

- **`ALGORITHM`**: 
  - Description: The algorithm used for encoding the JWT tokens. The default value is `HS256`.
  - Example: `ALGORITHM="HS256"`

- **`ACCESS_TOKEN_EXPIRE_MINUTES`**: 
  - Description: The duration (in minutes) for which the access token is valid. Adjust this value according to your application's needs.
  - Example: `ACCESS_TOKEN_EXPIRE_MINUTES=30`

#### Database Configuration

- **`MONGODB_URL`**: 
  - Description: The URL connection string for your MongoDB instance. This typically includes the protocol, host, and port.
  - Example: `MONGODB_URL="mongodb://localhost:27017/"`

- **`MONGODB_USERNAME`**: 
  - Description: The username for authenticating with your MongoDB database, if applicable.
  - Example: `MONGODB_USERNAME="your_username"`

- **`MONGODB_PASSWORD`**: 
  - Description: The password for the specified MongoDB user.
  - Example: `MONGODB_PASSWORD="your_password"`

- **`MONGODB_HOST`**: 
  - Description: The host and port for the MongoDB database. Default is `localhost:27017`.
  - Example: `MONGODB_HOST="localhost:27017"`

- **`MONGO_DATABASE`**: 
  - Description: The name of the MongoDB database to be used by the application.
  - Example: `MONGO_DATABASE="clean-database"`

- **`MONGO_COLLECTION_USERS`**: 
  - Description: The name of the MongoDB collection where user data will be stored.
  - Example: `MONGO_COLLECTION_USERS="user-collection"`

- **`MONGODB_MAX_CONNECTIONS_COUNT`**: 
  - Description: The maximum number of connections allowed to the MongoDB database.
  - Example: `MONGODB_MAX_CONNECTIONS_COUNT=20`

- **`MONGODB_MIN_CONNECTIONS_COUNT`**: 
  - Description: The minimum number of connections to maintain in the connection pool.
  - Example: `MONGODB_MIN_CONNECTIONS_COUNT=1`

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

- [ ] complete Tests

- [x] implement Authentication

- [ ] logging system

- [ ] cache system
