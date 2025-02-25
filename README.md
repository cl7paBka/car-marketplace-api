# 🚗 Car Marketplace API

<a href="https://github.com/cl7paBka/car-marketplace-api/blob/main/README.md"><img alt="README in English" src="https://img.shields.io/badge/English-purple"></a>
<a href="https://github.com/cl7paBka/car-marketplace-api/blob/main/readme_assets/README_ru.md"><img alt="README in Russian" src="https://img.shields.io/badge/Русский-purple"></a>

Welcome to **car-marketplace-api**, my personal **pet project** that showcases my growing expertise in building **RESTful API**s with modern frameworks and libraries. This service provides a robust **back-end** for managing users, car listings, and orders — making it both easy to maintain and straightforward to scale as the project evolves.

---

## 🔍 Project Overview

**Technology Stack**:

- 🐍 **Python** 3.11 Version
- ⚡ **FastAPI** – Framework for building high-performance APIs
- 🗃️ **SQLAlchemy 2+** – ORM that simplifies database operations and abstracts away raw SQL.
- 🐘 **PostgreSQL** – A rock-solid relational database solution.
- 📊 **Pydantic** – – Ensures data validation and schema management are both transparent and efficient.
- 🐳 **Docker** & **Docker Compose** – Containerization tools that make deployment smoother and more portable.
- 🧪 **Pytest** – For robust testing, helping maintain code quality and reliability.

---

## 🚀 Setup and Launch

The project is fully containerized and ready to run with **Docker** and **Docker Compose**. Follow the steps below to get it up and running:
1. **Clone the repository**:

   ```bash
   git clone https://github.com/cl7paBka/car-marketplace-api.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd car-marketplace-api
   ```
3. **Copy and rename `example.env` to `.env`**, make sure to **change the default database password** in this file for security purposes.
   - **Windows**
   ```bash
   copy example.env .env
   ```
   - **Linux/macOS**
   ```bash
   cp example.env .env
   ```
   
4. **Install Docker and Docker Compose**, if you haven’t already:

   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

5. **Launch the project**:

   ```bash
   docker-compose up --build
   ```

    Once setup is complete, you can access the API server at http://localhost:8000.

6. **Explore the API Documentation**

    FastAPI provides automatic Swagger docs. You can access them at http://localhost:8000/docs. 
This interactive interface lets you test all available endpoints directly from your browser.

<details>
  <summary style="font-size: 1.5em; font-weight: bold; color: #007A7C;">Click to view images of Docs</summary>
    <img src="https://i.postimg.cc/2SxrRnfw/image.png" width="1000px" alt="Users end-points"/>
    <img src="https://i.postimg.cc/9z3Nzgy7/image.png" width="1000px" alt="Cars end-points"/>
    <img src="https://i.postimg.cc/h4JDzJ9D/image.png" width="1000px" alt="Orders end-points"/>

</details>

## 🧪 Running Tests

This project includes a comprehensive test suite that covers all endpoints positive and negative cases — to ensure full functionality and reliability. To run the tests, follow these steps:

1. **Ensure the Docker containers are running.**  
   If not already running, start them with:
   ```bash
   docker-compose up --build
   ```
2. **Open a shell in the running application container:**
   ```bash
   docker exec -it car-marketplace-app bash
   ```
3. **Run the tests**
- To run all tests:
   ```bash
   pytest
   ```
- To run tests with coverage analysis:
   ```bash
   pytest --cov
   ```
  
  <details>
  <summary style="font-size: 1.5em; font-weight: bold; color: #007A7C;">Click to view images of Test Coverage</summary>
    <img src="https://i.postimg.cc/1X61WqHD/image.png" width="1000px" alt="Test coverage"/>

  </details>
  
---

## 💫 Key Features and Endpoints

This API revolves around three primary entities, each with its own set of attributes and operations. 

### Entities

1. **Users**  
   - **Roles:** `customer`, `manager`, `admin`  
   - **Actions:** Create, retrieve, update, and delete user accounts.

2. **Cars**  
   - **Engine Types:** `gasoline`, `electric`, `diesel`  
   - **Transmissions:** `manual`, `automatic`  
   - **Actions:** Add, view, edit, and remove car listings.

3. **Orders**  
   - **Status Types:** `pending`, `completed`, `canceled`  
   - **Actions:** Create, retrieve, update, and delete order records.

All important attributes within these entities have dedicated **GET** methods to retrieve their values efficiently.

### CRUD Operations

Each of these entities supports the following methods to manage data:

- **GET** – Retrieve data (e.g., list all cars, fetch user details, or get a specific attribute).  
- **POST** – Create new records (e.g., add a new user, car listing, or order).  
- **PATCH** – Partially update existing records (e.g., update only the user’s email, change just the car’s price, or modify the status of an order).  
- **DELETE** – Remove records from the system (e.g., delete a user or car listing).

By supporting **PATCH** requests, the API allows you to update specific fields without overwriting the entire record — making it more efficient and safer for incremental changes.

---
## 🏗️ Project Architecture

This project adopts an **onion architecture** to achieve a clear separation of concerns, where each layer encapsulates a specific part of the application. By doing so, inner layers (models, business logic) remain stable and independent of changes in outer layers (APIs, infrastructure). Below is an overview of the core patterns and structural choices that make this codebase both clean and maintainable.

### Onion Architecture Overview
- **Domain and Models** (`Innermost Layer`): Defines the core structures (e.g., `User, Car, Order) and business rules that remain independent of any external services or frameworks.  
- **Repositories and Services** (`Middle Layer`): Encapsulate data operations and application logic, ensuring a well-defined interface between how data is stored and how it’s used.  
- **API (Routing Layer)** (`Outer Layer`): Handles HTTP requests and responses, delegating business logic to services and data persistence to repositories.  
- **Infrastructure** (`Outermost Layer`): Covers everything from configuration and environment management to containerization, enabling smooth deployments across different setups.

### Key Patterns

- **Repository Pattern**  
  Each repository (e.g., `cars.py`, `orders.py`, `users.py`) focuses on database interactions. This keeps data access logic separate from business logic, making the application more modular and test-friendly.

- **Layered (Onion) Architecture**  
  Different layers handle different concerns: routing (`api`), data handling (`db`), data validation (`schemas`), and configuration (`config.py`). This modular approach ensures that changes in one layer have minimal impact on other parts of the system.

- **Dependency Injection**  
  FastAPI’s dependency injection feature (implemented in `dependencies.py`) allows the straightforward injection of database sessions and repositories into route handlers. This leads to loosely coupled components and more maintainable code.

- **Configuration Management**  
  The `config.py` file, combined with environment variables specified in `example.env`, centralizes settings for database URLs, secret keys, and other crucial configurations. This helps keep the application consistent across development, staging, and production.

- **Containerization**  
  Using **Docker** and **Docker Compose**, the entire app can be packaged and deployed in any environment with minimal effort—removing the “it works on my machine” problem and providing a scalable, reproducible setup.

---

### 🗂️ Directory Structure

```bash
car-marketplace-api/
├── docker-compose.yml         # Defines multiple services (app, db, etc.) for easy setup
├── Dockerfile                 # Builds the Docker image for the FastAPI application
├── example.env                # Example file for environment variables 
├── main.py                    # Application entry point, initializes FastAPI app and includes routers
├── pytest.ini                 # Configuration for Pytest 
├── readme_assets
│   └── README_ru.md           # Additional documentation in Russian
├── README.md                  # Main project documentation
├── requirements.txt           # Lists all Python dependencies needed for the project
├── src
│   ├── api                    # Layer for HTTP endpoints, request handling, and route definitions
│   │   ├── dependencies.py    # FastAPI dependencies for injecting DB sessions, repos, etc.
│   │   ├── __init__.py
│   │   ├── responses
│   │   │   ├── cars_responses.py   # Response models & structures specifically for Cars
│   │   │   ├── orders_responses.py # Response models & structures specifically for Orders
│   │   │   └── users_responses.py  # Response models & structures specifically for Users
│   │   ├── routers.py         # Combines all routes into a single router to include in main.py
│   │   └── routes
│   │       ├── cars.py        # Car-related endpoints 
│   │       ├── __init__.py
│   │       ├── orders.py      # Order-related endpoints 
│   │       └── users.py       # User-related endpoints 
│   ├── db
│   │   ├── db.py              # Database initialization (SQLAlchemy session, engine, etc.)
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models
│   │   └── models.py          # SQLAlchemy model definitions (User, Car, Order)
│   ├── repositories
│   │   ├── cars.py            # Database operations for Cars 
│   │   ├── orders.py          # Database operations for Orders
│   │   └── users.py           # Database operations for Users
│   ├── schemas
│   │   ├── base_response.py   # Shared response schemas for consistency
│   │   ├── cars.py            # Pydantic schemas for Cars 
│   │   ├── orders.py          # Pydantic schemas for Orders
│   │   └── users.py           # Pydantic schemas for Users
│   ├── services
│   │   ├── cars.py            # Business logic for Car-related operations 
│   │   ├── orders.py          # Business logic for Order-related operations
│   │   └── users.py           # Business logic for User-related operations
│   └── utils
│       ├── config.py          # Central config handling (reads from env variables, sets defaults)
│       ├── enums.py           # Enums for constants (like engine types, roles, etc.)
│       ├── exception_handler.py # Custom exceptions & error handling
│       └── repository.py      # Base repository functionality (common DB operations)
└── tests
    ├── conftest.py            # Setup for Pytest fixtures 
    ├── __init__.py
    ├── test_api
    │   └── test_routes
    │       ├── test_cars.py   # Tests for Car endpoints
    │       ├── test_orders.py # Tests for Order endpoints
    │       └── test_users.py  # Tests for User endpoints
    └── utils
        ├── config.py          # Test-specific configs 
        └── __init__.py
```

### Why this architecture❔
I chose an **onion 🧅 (layered) architecture** because it keeps each part of the application focused on its own responsibilities, making it simpler to modify or replace individual layers without disrupting the entire system. By having clear boundaries between routing, business logic, and data persistence, you can:

1. **Scale More Easily** – You can update or swap out specific layers (e.g., change the database from PostgreSQL to another solution) without rewriting everything.
2. **Test More Effectively** – Each layer is isolated, so you can test your data logic independently from the API endpoints.
3. **Maintain Cleaner Code** – Because there’s a clear separation of concerns, it’s easier to navigate the codebase and locate the exact logic that needs attention.

In short, this architecture helps ensure a solid foundation that’s ready for growth and straightforward to maintain over the long run.

---

✨ Thank you for checking out **car-marketplace-api**! ✨

Feel free to reach out with any questions or suggestions.