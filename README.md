# Tech Stack

Backend: FastAPI  
Database: PostgreSQL  
ORM: SQLAlchemy  
Frontend: HTML, CSS, JavaScript  
Containerization: Docker  

# How to Run the HR API (English)

Docker must be installed before running the project.
Use the following commands:

> sudo apt update
> sudo apt install -y docker.io docker-compose
> sudo systemctl enable --now docker

Run this command in the project folder:
> docker compose up --build

After opening the UI at http://localhost:3000, you can use the following features:

User is able to add, update and delete department/employee information.

- Department Management
    - The user can change the name and location of the department.

- Employee Management
    - User is able to change the name, surname, salary, email, start date and the department the employee works in.
    - The user can select a department from a dropdown menu.
    - User can select a start date from the calendar.

All changes are automatically saved to the database, and the UI updates in real-time.

Use the following command to stop the project:
> docker compose down

# Project Structure

hr_api
├── app
│ ├── config.py
│ ├── database.py
│ ├── dependencies.py
│ ├── main.py
│ ├── models.py
│ ├── repositories
│ │ ├── __init__.py
│ │ ├── base_repository.py
│ │ ├── department_repository.py
│ │ └── employee_repository.py
│ ├── routers
│ │ ├── departments.py
│ │ └── employees.py
│ ├── schemas.py
│ └── services
│   ├── __init__.py
│   ├── department_service.py
│   └── employee_service.py
│
├── frontend
│ ├── Dockerfile
│ ├── app.js
│ ├── favicon.png
│ ├── index.html
│ └── style.css

# Code Structure

The backend follows a layered architecture to separate responsibilities and keep the code maintainable and scalable.

```
Client (Frontend)
        │
        ▼
Routers (API Layer)
        │
        ▼
Services (Business Logic)
        │
        ▼
Repositories (Database Access)
        │
        ▼
Database (PostgreSQL)
```

## Routers

Routers define the HTTP endpoints.
They receive requests from the frontend, validate input using schemas, and call the appropriate service functions.

## Services

Services contain the core business logic of the application.
They process data and coordinate operations between routers and repositories.

## Repositories

Repositories are responsible for interacting with the database using SQLAlchemy.

## Schemas

Schemas define Pydantic models used for operations.

## Models

Models represent the database tables.

## Dependencies

Dependencies handle API key verification and database session injection.

## Database Configuration

Database configuration handles database connection, SQLAlchemy session creation and environment configuration.

## A Request Example Flow

1. Frontend sends POST /employees
2. employees.py router receives the request
3. Router calls employee_service.create_employee()
4. Service processes the logic and calls the repository
5. Repository inserts the employee into PostgreSQL
6. Response is returned to the client


# HR API Nasıl Çalıştırılır (Türkçe)

Projeyi çalıştırmadan önce Docker'ın yüklü olması gerekmektedir.
Docker'ı yüklemek için aşağıdaki komutları kullanabilirsiniz:

> sudo apt update
> sudo apt install -y docker.io docker-compose
> sudo systemctl enable --now docker

Proje klasörünün içinde aşağıdaki komutu çalıştırın:
> docker compose up --build

Arayüzü http://localhost:3000 adresinde açtıktan sonra aşağıdaki özellikleri kullanabilirsiniz:

Kullanıcı sistemde departman ve çalışan bilgilerini ekleyebilir, güncelleyebilir ve silebilir.

- Departman Yönetimi
    - Kullanıcı departmanın adını ve konumunu değiştirebilir.

- Çalışan Yönetimi
    - Kullanıcı çalışanın adını, soyadını, maaşını, e-postasını, işe başlama tarihini ve çalıştığı departmanı değiştirebilir.
    - Kullanıcı açılır menüden (dropdown) bir departman seçebilir.
    - Kullanıcı takvimden bir işe başlama tarihi seçebilir.

Yapılan tüm değişiklikler otomatik olarak veritabanına kaydedilir ve arayüz gerçek zamanlı olarak güncellenir.

Projeyi durdurmak için aşağıdaki komutu kullanabilirsiniz:
> docker compose down

# Proje Mimarisi

hr_api
├── app
│ ├── config.py
│ ├── database.py
│ ├── dependencies.py
│ ├── main.py
│ ├── models.py
│ ├── repositories
│ │ ├── __init__.py
│ │ ├── base_repository.py
│ │ ├── department_repository.py
│ │ └── employee_repository.py
│ ├── routers
│ │ ├── departments.py
│ │ └── employees.py
│ ├── schemas.py
│ └── services
│   ├── __init__.py
│   ├── department_service.py
│   └── employee_service.py
│
├── frontend
│ ├── Dockerfile
│ ├── app.js
│ ├── favicon.png
│ ├── index.html
│ └── style.css

# Kod Mimarisi

```
Client (Frontend)
        │
        ▼
Routers (API Layer)
        │
        ▼
Services (Business Logic)
        │
        ▼
Repositories (Database Access)
        │
        ▼
Database (PostgreSQL)
```

## Router'lar

Router'lar HTTP endpointlerini tanımlar.
Frontend'den gelen istekleri alır, schema'lar kullanarak input'ları doğrular ve uygun service fonksiyonlarını çağırır.

## Servisler

Servisler uygulamanın temel iş mantığını içerir.
Verileri işler ve router ile repository katmanları arasındaki işlemleri koordine eder.

## Repository'ler

Repository'ler SQLAlchemy kullanarak veritabanı ile etkileşim kurmaktan sorumludur.

## Schema'lar

Schema'lar işlemler için kullanılan Pydantic modellerini tanımlar.

## Modeller

Modeller veritabanı tablolarını temsil eder.

## Bağımlılıklar

Dependencies API anahtarı doğrulamasını ve veritabanı oturumu enjeksiyonunu yönetir.

## Veritabanı Yapılandırması

Veritabanı yapılandırması veritabanı bağlantısını, SQLAlchemy oturumu oluşturmayı ve ortam yapılandırmasını yönetir.

## Kullanım Örneği

1. Frontend POST /employees isteği gönderir
2. employees.py router isteği alır
3. Router employee_service.create_employee() fonksiyonunu çağırır
4. Service iş mantığını işler ve repository katmanını çağırır
5. Repository çalışanı PostgreSQL veritabanına ekler
6. Yanıt istemciye döndürülür

