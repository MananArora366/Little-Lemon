# Little Lemon Restaurant — Backend API

A RESTful backend for the Little Lemon restaurant built with **Django** and **Django REST Framework (DRF)**.

---

## 🍋 Features
- **Menu Management**: List, create, retrieve, update, and delete menu items with title, price, and inventory tracking.
- **Table Booking API**: Full CRUD table reservations management via DRF `ModelViewSet`.
- **Admin Interface**: Integrated Django Admin with custom search filters for Menu and Bookings.
- **Unit Testing**: Automated test suite for models and REST endpoints (`python manage.py test`).

---

## 🛠️ Tech Stack
- **Framework**: Django 6.1
- **API Engine**: Django REST Framework 3.18
- **Database**: SQLite3
- **Language**: Python 3.12+

---

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Run Automated Tests
```bash
python manage.py test
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 📋 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Restaurant Landing Page (HTML) |
| `GET`, `POST` | `/menu/` | List all menu items or create a new item |
| `GET`, `PUT`, `DELETE` | `/menu/<id>` | Retrieve, update, or remove a single menu item |
| `GET`, `POST` | `/restaurant/booking/tables/` | View and create table bookings |
| `GET`, `PUT`, `DELETE` | `/restaurant/booking/tables/<id>/` | View, update, or cancel specific booking |
| `GET` | `/admin/` | Django Admin Dashboard |

---

## 🏛️ Project Architecture
```text
littlelemon/
├── littlelemon/           # Project configuration & root routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── restaurant/            # Core restaurant application
│   ├── models.py          # Menu & Booking models
│   ├── serializers.py     # DRF ModelSerializers
│   ├── views.py           # Template views & DRF API views
│   ├── urls.py            # App-level routing
│   ├── templates/         # HTML Landing Page
│   └── tests.py           # Model and API unit tests
├── db.sqlite3             # SQLite Database
├── manage.py              # Django management script
└── requirements.txt       # Pinned dependencies
```
