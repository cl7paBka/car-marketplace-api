# 🚗 Car Marketplace API

<a href="https://github.com/cl7paBka/car-marketplace-api/blob/main/README.md"><img alt="README in English" src="https://img.shields.io/badge/English-purple"></a>
<a href="https://github.com/cl7paBka/car-marketplace-api/blob/main/readme_assets/README_ru.md"><img alt="README in Russian" src="https://img.shields.io/badge/Русский-purple"></a>

Добро пожаловать в **car-marketplace-api** — мой персональный **pet-проект**, который демонстрирует мой растущий опыт в создании **RESTful API** с использованием современных фреймворков и библиотек. Этот сервис предоставляет надежный **бэкенд** для управления пользователями, объявлениями об автомобилях и заказами, обеспечивая простоту поддержки и удобство масштабирования по мере развития проекта.

---

## 🔍 Краткий обзор

**Стек технологий**:

- 🐍 **Python** версии 3.11  
- ⚡ **FastAPI** – фреймворк для высокопроизводительных API  
- 🗃️ **SQLAlchemy 2+** – ORM, упрощающая операции с базой данных и абстрагирующая сложные SQL-запросы  
- 🐘 **PostgreSQL** – надежная реляционная база данных  
- 📊 **Pydantic** – гарантирует прозрачную и эффективную валидацию данных и управление схемами  
- 🐳 **Docker** и **Docker Compose** – инструменты контейнеризации, упрощающие развертывание и делающие его более гибким  
- 🧪 **Pytest** – обеспечивает надежное тестирование, поддерживая качество и стабильность кода  

---

## 🚀 Установка и запуск

Проект полностью контейнеризирован и готов к запуску с помощью **Docker** и **Docker Compose**. Для этого выполните следующие шаги:
1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/cl7paBka/car-marketplace-api.git
   ```

2. **Перейдите в директорию проекта**:

   ```bash
   cd car-marketplace-api
   ```
3. **Скопируйте и переименуйте файл `example.env` в `.env`**, обязательно **измените пароль** к базе данных в этом файле для обеспечения безопасности.
   - **Windows**
   ```bash
   copy example.env .env
   ```
   - **Linux/macOS**
   ```bash
   cp example.env .env
   ```
   
4. **Установите Docker и Docker Compose**, если они еще не установлены:

   - [Руководство по установке Docker](https://docs.docker.com/get-docker/)
   - [Руководство по установке Docker Compose](https://docs.docker.com/compose/install/)

5. **Запустите проект**:

   ```bash
   docker-compose up --build
   ```

    После успешной сборки и запуска, API-сервер будет доступен по адресу: http://localhost:8000.

6. **Ознакомьтесь с документацией API**

    FastAPI автоматически генерирует документацию Swagger. Она доступна по адресу:
http://localhost:8000/docs
Этот интерфейс позволяет взаимодействовать со всеми энд-поинтами прямо в браузере.

<details>
  <summary style="font-size: 1.5em; font-weight: bold; color: #007A7C;">Нажмите, чтобы посмотреть изображения документации</summary>
    <img src="https://i.postimg.cc/2SxrRnfw/image.png" width="1000px" alt="Users end-points"/>
    <img src="https://i.postimg.cc/9z3Nzgy7/image.png" width="1000px" alt="Cars end-points"/>
    <img src="https://i.postimg.cc/h4JDzJ9D/image.png" width="1000px" alt="Orders end-points"/>

</details>

## 🧪 Запуск тестов

В проекте предусмотрен обширный набор тестов, покрывающих все позитивные и негативные сценарии для проверки функциональности и надежности. Чтобы запустить тесты, следуйте инструкциям ниже:

1. **Убедитесь, что Docker-контейнеры запущены**.  
   Если они не активны, выполните:
   ```bash
   docker-compose up --build
   ```
2. **Откройте консоль внутри запущенного контейнера**:
   ```bash
   docker exec -it car-marketplace-app bash
   ```
3. **Запустите тесты:**
- Запуск всех тестов:
   ```bash
   pytest
   ```
- Запуск тестов с анализом покрытия:
   ```bash
   pytest --cov
   ```
  
  <details>
  <summary style="font-size: 1.5em; font-weight: bold; color: #007A7C;">Нажмите, чтобы посмотреть изображения покрытия тестами</summary>
    <img src="https://i.postimg.cc/1X61WqHD/image.png" width="1000px" alt="Test coverage"/>

  </details>
  
---

## 💫 Основные возможности и энд-поинты

Данный API построен вокруг трех основных сущностей, каждая из которых имеет свой набор атрибутов и действий.
### Сущности

1. **Users**  
   - **Роли:** `customer`, `manager`, `admin`  
   - **Действия:** создание, получение, обновление и удаление учетных записей.

2. **Cars**  
   - **Типы двигателей:** `gasoline`, `electric`, `diesel`  
   - **Трансмиссия:** `manual`, `automatic`  
   - **Действия:** добавление, просмотр, редактирование и удаление объявлений

3. **Orders**  
   - **Статусы:** `pending`, `completed`, `canceled`  
   - **Действия:** создание, получение, обновление и удаление заказов

Все важные атрибуты в этих сущностях могут быть получены с помощью специальных методов **GET**, которые облегчают доступ к нужной информации.
### CRUD-операции

Для каждой из перечисленных сущностей доступны следующие операции:

- **GET** – получение данных (например, список всех автомобилей, информация о пользователе или конкретном атрибуте).
- **POST** – создание новых записей (например, нового пользователя, объявления об автомобиле или заказа).
- **PATCH** – частичное обновление существующих записей (например, изменение только email у пользователя, цены у автомобиля или статуса заказа).
- **DELETE** – удаление записей (например, пользователя или объявления).

Поддержка **PATCH** позволяет обновлять отдельные поля, не перезаписывая всю запись, что делает взаимодействие с данными более гибким и безопасным.

---
## 🏗️ Архитектура проекта

В этом проекте реализован подход **onion architecture**, который обеспечивает четкое разделение ответственности. Каждый слой инкапсулирует определенную логику приложения, сохраняя стабильность и независимость внутренних слоев (модели, бизнес-логика) от внешних (API, инфраструктура). Ниже приведен обзор основных шаблонов и структурных решений, делающих код удобным для чтения и сопровождения.
### Общая схема onion-архитектуры
- **Домен и модели** (`внутренний слой`): определяют основные структуры (например, User, Car, Order) и бизнес-правила, которые не зависят от внешних сервисов или фреймворков.
- **Repositories and Services** (`средний слой`): отвечают за операции с данными и бизнес-логику, разграничивая способы хранения данных и их использования.
- **API (Routing Layer)** (`внешний слой`): обрабатывает HTTP-запросы и ответы, делегируя бизнес-логику сервисам, а взаимодействие с базой — репозиториям.
- **Infrastructure** (`самый внешний слой`): включает в себя конфигурацию, управление окружением и контейнеризацию, позволяя легко деплоить проект в различных средах.

### Основные паттерны

- **Паттерн "Репозиторий"**  
  Каждый репозиторий (например, `cars.py`, `orders.py`, `users.py`) занимается взаимодействием с базой данных, изолируя логику доступа к данным от бизнес-логики.
- **Многослойная (луковая) архитектура**
  Различные слои решают свои задачи: маршрутизация (`api`), управление данными (`db`), валидация (`schemas`), конфигурация (`config.py`) и т.д. Это обеспечивает минимальное влияние изменений в одном слое на другие.
- **Внедрение зависимостей**  
  Механизм Dependency Injection в FastAPI (реализованный в `dependencies.py`) упрощает передачу сессий базы данных и репозиториев в функции-обработчики. Компоненты получаются слабо связанными и проще в сопровождении.
- **Управление конфигурацией**  
  Файл `config.py` и переменные окружения, указанные в `example.env`, позволяют централизованно управлять настройками (например, URL к базе данных, секретные ключи и т. д.) и поддерживать единообразие между разными средами (разработка, тестирование, продакшн).
- **Контейнеризация**  
  С помощью **Docker** и **Docker Compose** всё приложение пакуется в контейнер, что упрощает развертывание и гарантирует единообразие окружения на разных платформах.

---

### 🗂️ Directory Structure

```bash
car-marketplace-api/
├── docker-compose.yml         # Описывает несколько сервисов (приложение, БД и т.д.) для быстрого запуска
├── Dockerfile                 # Содержит инструкции по сборке Docker-образа с приложением FastAPI
├── example.env                # Пример файла окружения
├── main.py                    # Точка входа в приложение, инициализирует FastAPI и подключает роутеры
├── pytest.ini                 # Конфигурация для Pytest
├── readme_assets
│   └── README_ru.md           # Дополнительная документация на русском
├── README.md                  # Основная документация
├── requirements.txt           # Список всех Python-зависимостей
├── src
│   ├── api                    # Слой, отвечающий за HTTP-эндпоинты, обработку запросов и маршрутизацию
│   │   ├── dependencies.py    # Зависимости FastAPI (сессии БД, репозитории и т.д.)
│   │   ├── __init__.py
│   │   ├── responses
│   │   │   ├── cars_responses.py   # Модели ответов, специфичные для автомобилей
│   │   │   ├── orders_responses.py # Модели ответов, специфичные для заказов
│   │   │   └── users_responses.py  # Модели ответов, специфичные для пользователей
│   │   ├── routers.py         # Объединяет все маршруты в единый роутер для подключения в main.py
│   │   └── routes
│   │       ├── cars.py        # Эндпоинты, связанные с автомобилями
│   │       ├── __init__.py
│   │       ├── orders.py      # Эндпоинты, связанные с заказами
│   │       └── users.py       # Эндпоинты, связанные с пользователями
│   ├── db
│   │   ├── db.py              # Инициализация базы данных (SQLAlchemy session, engine и т.д.)
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models
│   │   └── models.py          # Определения моделей SQLAlchemy (User, Car, Order)
│   ├── repositories
│   │   ├── cars.py            # Операции с БД, связанные с автомобилями
│   │   ├── orders.py          # Операции с БД, связанные с заказами
│   │   └── users.py           # Операции с БД, связанные с пользователями
│   ├── schemas
│   │   ├── base_response.py   # Общие схемы ответов для единообразия
│   │   ├── cars.py            # Схемы Pydantic для автомобилей
│   │   ├── orders.py          # Схемы Pydantic для заказов
│   │   └── users.py           # Схемы Pydantic для пользователей
│   ├── services
│   │   ├── cars.py            # Бизнес-логика, связанная с автомобилями
│   │   ├── orders.py          # Бизнес-логика, связанная с заказами
│   │   └── users.py           # Бизнес-логика, связанная с пользователями
│   └── utils
│       ├── config.py          # Центральное управление конфигурацией (чтение env-переменных, установка значений по умолчанию)
│       ├── enums.py           # Перечисления (engine types, roles и т.д.)
│       ├── exception_handler.py # Кастомные исключения и обработка ошибок
│       └── repository.py      # Базовый функционал репозитория (общие операции с БД)
└── tests
    ├── conftest.py            # Настройки для Pytest-fixture
    ├── __init__.py
    ├── test_api
    │   └── test_routes
    │       ├── test_cars.py   # Тесты эндпоинтов для автомобилей
    │       ├── test_orders.py # Тесты эндпоинтов для заказов
    │       └── test_users.py  # Тесты эндпоинтов для пользователей
    └── utils
        ├── config.py          # Конфигурация, специфичная для тестов
        └── __init__.py
```
### Почему именно эта архитектура❔
Я выбрал **луковую 🧅 (слоеную) архитектуру**, так как она разделяет приложение на четкие слои, каждый из которых отвечает за свою задачу. Это упрощает процесс изменения или замены отдельных компонентов без необходимости переписывать всю систему. Четкое разграничение между маршрутизацией (API), бизнес-логикой и хранением данных даёт несколько преимуществ:

1. **Упрощенное масштабирование** – можно заменить или обновить конкретный слой (например, сменить базу данных с PostgreSQL на другую) без переписывания всей кодовой базы.
2. **Эффективное тестирование** – каждый слой изолирован, благодаря чему тестировать бизнес-логику отдельно от эндпоинтов API намного проще.
3. **Более чистый код** – поскольку обязанности разделены, проще ориентироваться в проекте и быстро находить нужную логику.

Таким образом, данная архитектура закладывает прочный фундамент, который легко расширять и поддерживать на протяжении долгого времени.

---

✨ Спасибо, что ознакомились с **car-marketplace-api**! ✨

Если у вас есть какие-либо вопросы или предложения, буду рад обратной связи.