# ByteProwler Contact API (Django)

A simple Django REST API that powers the contact form on my portfolio website.
It accepts contact messages and sends them to my email using Resend.

## Live URL
- API Base URL: https://byteprowler-contact.onrender.com

## Tech Stack
- Django
- Django REST Framework
- django-cors-headers
- Whitenoise (static files on Render)
- Gunicorn (production server)
- Resend (email sending)

---

## Features
- Contact form endpoint (POST)
- Email delivery via Resend
- CORS configured for portfolio frontend
- Render deployment ready

---

## API Endpoints

### `POST /api/contact/send/`
Send a contact message.

#### Request Body (JSON)
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Project inquiry",
  "message": "Hello, I’d like to work with you."
}
