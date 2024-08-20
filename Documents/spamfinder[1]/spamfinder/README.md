# Phonebook REST API

## Overview

This project implements a REST API for a phonebook application. It allows users to register, log in, search for contacts by name or phone number, and mark numbers as spam. The backend is built using Django and uses a relational database for data persistence.

## Features

- User Registration
- User Login
- Search by Name
- Search by Phone Number
- Mark Number as Spam

## Models

### User

The `User` model is a custom user model that extends `AbstractBaseUser` and `PermissionsMixin`. It includes fields for name, email, phone number, password, and administrative flags.

**Fields:**
- `name`: `CharField`
- `email`: `EmailField`
- `phone_number`: `CharField`
- `is_active`: `BooleanField`
- `is_admin`: `BooleanField`

### Contact

The `Contact` model represents a user's contact and includes fields for the contact's name and phone number.

**Fields:**
- `name`: `CharField`
- `phone_number`: `CharField`

### SpamReport

The `SpamReport` model keeps track of phone numbers marked as spam and how many times they've been reported.

**Fields:**
- `phone_number`: `CharField`
- `report_count`: `IntegerField`

## Serializers

Custom serializers are used to convert model instances to JSON data.

### UserSerializer

Serializes the `User` model.

### ContactSerializer

Serializes the `Contact` model.

### SpamReportSerializer

Serializes the `SpamReport` model.

## Views

### User Registration

Registers a new user.

**Endpoint:** `/api/register/`  
**Method:** `POST`

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "1234567890",
    "password": "password123"
}

**Response**
```json
{
  "message": "User registered successfully"
}
```

User Login

Logs in a user.

**Endpoint:** `/api/login/`
**Method:** `POST`

**Request Body:**
```json
{
    "number": "8392834723",
    "password": "password123"
}
```

**Response**
```json
{
  "message": "Login successful"
}
```

Search by Name

Searches for users and contacts by name.

**Endpoint:** `/api/search/name/`
**Method:** `GET`

```json
{
  "name": "hello"
}
```

```json
{
  "contacts": [
    {
      "name": "vivek"
    },
    {
      "name": "abv"
    }
  ]
}
```

Search by Phone Number

Searches for users and contacts by phone number.

**Endpoint:** `/api/search/phone_number/`
**Method:** `GET`

```json
{
  "name": "hello"
}
```

Response

```json
{
  "contacts": [
    {
      "name": "viv"
    }
  ],
  "spam_count": 1
}
```


Mark Number as Spam

Marks a phone number as spam.

**Endpoint:** `/api/mark_as_spam/`
**Method:** `POST`


Request Body:
```json
{
    "phone_number": "1234567890"
}
```

Response:
```json
{
    "phone_number": "1234567890",
    "report_count": 1
}
```

---

Installation and Setup
Prerequisites

  Python 3.x
  Django 3.x or 4.x
  A relational database (e.g., SQLite, PostgreSQL, MySQL)

Installation

  

Create and activate a virtual environment:

```bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the dependencies:

```bash

pip install -r requirements.txt
```

Configure the database settings in phonebook_project/settings.py.

Run migrations:

```bash

python manage.py makemigrations
python manage.py migrate
```

Create a superuser:

```bash

python manage.py createsuperuser
```

Start the development server:

```bash

  python manage.py runserver
```
Accessing the Admin Interface

  Navigate to http://localhost:8000/admin/.
  Log in using the superuser credentials you created.

Testing the API

Use tools like Postman or Curl to test the API endpoints. Below are some example requests.
Register a User

Endpoint: `/api/register/`
Method: `POST`

Request Body:

```json

{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "1234567890",
    "password": "password123"
}
```

Log in a User

Endpoint: `/api/login/`
Method: `POST`

Request Body:

```json

{
    "email": "john.doe@example.com",
    "password": "password123"
}
```

Search by Name

Endpoint: `/api/search/name/`
Method: `POST`

```json

{
    "name": "hel"
}
```

Search by Phone Number

Endpoint: `/api/search/phone_number/`
Method: `POST`
Mark Number as Spam

Endpoint: `/api/mark_as_spam/`
Method: `POST`

Request Body:

```json

{
    "phone_number": "1234567890"
}
```

Authors

Vivek Mishra
