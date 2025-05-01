# 🎯 QR-Based Event Check-In API

A Django REST Framework API for managing event registrations, check-ins using QR codes, and exporting attendance data. Students can register and check in to events; hosts can create events, check in others, and export CSV summaries — all with secure JWT authentication.

---

## 🚀 Features

- ✅ Student and Host registration with roles
- 🔐 JWT-based authentication
- 📝 Event creation (host-only)
- 🎟️ Event registration (student-only)
- 📲 QR code-based check-in system via email
- 📂 CSV export of check-in records (host-only)
- 📊 Check-in summaries and listing endpoints
- 🔄 Clean REST API endpoints with proper separation of access (student/host)

---

## 🛠️ Tech Stack

- **Backend**: Django + Django REST Framework  
- **Auth**: JWT (JSON Web Tokens)  
- **Database**: SQLite (default, replaceable with PostgreSQL)  
- **QR**: `qrcode` library  
- **Email**: SMTP-based QR delivery (via Gmail, etc.)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Bhavy-official/qr-checkin-api.git
cd qr-checkin-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Migrate DB
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 📧 Email Configuration

This project sends QR codes and check-in confirmations via email using SMTP.

### ✅ Setup Steps

1. Create a `.env` file in the project root.
2. Add your email credentials:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

> ⚠️ For Gmail, use an [App Password](https://myaccount.google.com/apppasswords) instead of your normal password.

3. In `settings.py`, make sure to load these values:

```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

4. You can setup  Nodemailer or SendGrid if you want to


---

## 🔑 Authentication

All protected endpoints require JWT tokens.

1. Register and then log in via `/api/auth/login/`
2. Add this to your request headers:
```
Authorization: Bearer <your-token>
```

---

## 📚 API Endpoints

| Endpoint                                        | Method | Description                                             |
|-------------------------------------------------|--------|---------------------------------------------------------|
| `/api/auth/register/`                           | POST   | Register a new student or host                         |
| `/api/auth/login/`                              | POST   | Log in and get JWT token                               |
| `/api/events/create/`                           | POST   | Host creates a new event                               |
| `/api/events/list/`                             | GET    | List all events                                        |
| `/api/events/register/`                         | POST   | Student registers for an event                         |
| `/api/events/checkin/`                          | POST   | Check in to an event (students can check themselves in, hosts can check in others) |
| `/api/events/checkins/export/`                  | GET    | Export check-in data as CSV (host only)                |
| `/api/events/<int:event_id>/checkins/summary/`  | GET    | Get a summary of check-ins for an event (host only)    |


---

## 📬 Postman Docs

Check the [Postman Collection](https://bhavy-8544770.postman.co/workspace/Bhavy's-Workspace~7ac39ec4-cea2-4d34-83e2-72a9e450078e/collection/44590267-1dee5894-eed9-4e62-a21e-1c7d197f19df?action=share&creator=44590267) for full request examples, headers, and sample responses.


---

## ©️ Copyright

© 2025 Bhavy Manchanda. Feel free to use this project with appropriate credit.

---

## 🙌 Acknowledgements

```
Made by Bhavy Manchanda
Built with ❤️ using Django REST Framework.
```
---

