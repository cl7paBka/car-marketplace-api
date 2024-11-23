
# 🚗 Car Marketplace API

Welcome to **car-marketplace-api**! This project serves as the back-end for a car marketplace website, built using **FastAPI**. It enables essential functionalities for managing users, car listings, and orders, streamlining the development of a car marketplace platform.

---

## 🔍 Project Overview

**Technology Stack**:

- 🐍 **Python**
- ⚡ **FastAPI** – Framework for building APIs
- 🗃️ **SQLAlchemy 2+** – ORM for handling database interactions
- 📐 **Pydantic** – Data validation and schema management
- 🐘 **PostgreSQL** – Database solution
- 🐳 **Docker** & **Docker Compose** – For containerization and easy deployment

---

## 🛠️ Key Features and Endpoints

The API provides three main sets of endpoints:

1. **User** – Manage platform users, including creating, retrieving, updating, and deleting user accounts.
2. **Car** – Manage car listings, including adding, viewing, editing, and removing car details.
3. **Order** – Process car purchase orders, including creating, retrieving, updating, and deleting orders.


Each endpoint supports the following methods:

- **GET** – Retrieve data (e.g., list cars or get user info)
- **POST** – Create new records (e.g., a new user or car listing)
- **PATCH** – Update records partially (e.g., edit user data or car details)
- **DELETE** – Remove records (e.g., delete a car listing)


---

## 🏗️ Project Architecture

The project follows several design patterns to ensure clean, modular, and maintainable code.

### Key Patterns

- **Repository Pattern**: Database operations are encapsulated in repositories located in the `db/repositories` folder, ensuring a clean separation of data access logic and core business logic.
- **Layered Architecture**: Code is divided into layers for routing (`api`), database handling (`db`), data validation (`schemas`), and configuration (`config.py`), which promotes modularity and separation of concerns.
- **Dependency Injection**: FastAPI's dependency injection allows injection of database sessions and repositories into route handlers, improving modularity and facilitating testing.
- **Configuration Management**: The `config.py` file centralizes environment variables, simplifying configuration across development, staging, and production environments.
- **Containerization**: Docker and Docker Compose files allow consistent deployment across environments, making setup and scaling more reliable.

### 🗂️ Directory Structure

```Bash
car-marketplace-api/
│
├── src/                                # Source folder containing core logic
│   ├── api/                
│   │   ├── __init__.py                 # Initializes the api package
│   │   ├── car_routes.py               # Routes related to car operations
│   │   ├── order_routes.py             # Routes related to order operations
│   │   └── user_routes.py              # Routes related to user operations
│   ├── db/                        
│   │   ├── repositories/                
│   │   │   ├── car_repository.py       # Repository handling car data access
│   │   │   ├── order_repository.py     # Repository for order data operations
│   │   │   └── user_repository.py      # Repository for user data access
│   │   ├── __init__.py                 # Initializes the db package
│   │   └── models.py                   # ORM models representing database tables
│   ├── schemas/                
│   │   ├── car.py                      # Pydantic schemas for car validation
│   │   ├── order.py                    # Pydantic schemas for order validation
│   │   └── user.py                     # Pydantic schemas for user validation
│   └── config.py                       # Central configuration file
├── .dockerignore                       # Excludes files from Docker build
├── .gitignore                          # Excludes files from version control
├── docker-compose.yml                  # Docker Compose file to orchestrate containers
├── Dockerfile                          # Dockerfile defining the application image
├── main.py                             # Main entry point script to run 
├── README.md                           # Project overview, structure, and usage instructions
└── requirements.txt                    # Python dependencies file
```

---

## 🚀 Setup and Launch

The project is fully containerized and ready to launch using **Docker** and **Docker Compose**. Follow these steps to get started:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/car-marketplace-api.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd car-marketplace-api
   ```

3. **Install Docker and Docker Compose**, if you haven’t already:

   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

4. ❗ **Change passwords** for PostgreSQL database **in docker-compose.yml**! ❗

   ```yml
   services:
     db:
       ...
       environment:
         ...
         POSTGRES_PASSWORD: "5hA2RxS31dDhSrxn" # Change this before starting the project!
         ...
   
     app:
       ...
       environment:
         ...
         DATABASE_PASSWORD: "5hA2RxS31dDhSrxn" # Change this before starting the project!
         ...
   ```

5. **Start the project**:

   ```bash
   docker-compose up --build
   ```

Once setup is complete, you can access the API server at http://localhost:8000.

To explore the interactive API documentation powered by FastAPI’s automatic Swagger integration, visit http://localhost:8000/docs. This documentation provides a user-friendly interface for testing all available endpoints.

[![API documentation](https://i.postimg.cc/gknzQVZ6/NVIDIA-Share-n-OOXk-Kn-I0-N.png)](https://postimg.cc/7frrTTXx)

---


✨ Thank you for checking out **car-marketplace-api**! ✨

Feel free to reach out with any questions or suggestions.
