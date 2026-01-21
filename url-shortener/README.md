# Django URL Shortener Microservice

A production-ready URL shortener microservice built with Django REST Framework featuring Redis caching, PostgreSQL storage, and OpenAPI documentation.

## Features

- **REST API**: Create short URLs and redirect to original URLs
- **Redis Caching**: High-performance caching layer for frequently accessed URLs
- **PostgreSQL**: Reliable relational database storage
- **Analytics**: Track URL clicks and statistics
- **OpenAPI Documentation**: Interactive Swagger UI for API testing
- **Docker**: Fully containerized with docker-compose
- **Production-Ready**: Gunicorn WSGI server, CORS support, rate limiting

## Architecture

### Technology Stack
- **Django 5.0+** - Web framework
- **Django REST Framework** - API development
- **drf-spectacular** - OpenAPI/Swagger documentation
- **PostgreSQL** - Primary database
- **Redis** - Caching layer
- **Gunicorn** - WSGI server
- **Docker** - Containerization

### Project Structure
```
url-shortener/
├── manage.py
├── config/                  # Project settings
│   ├── settings/
│   │   ├── base.py         # Base settings
│   │   ├── development.py  # Dev settings
│   │   └── production.py   # Prod settings
│   ├── urls.py
│   └── wsgi.py
├── shortener/              # Main app
│   ├── models.py           # URL model
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── services.py         # Business logic
│   └── urls.py             # URL routing
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

##API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shorten/` | Create short URL |
| GET | `/<short_code>` | Redirect to original URL |
| GET | `/api/stats/<short_code>` | Get URL statistics |
| GET | `/api/docs/` | Swagger UI documentation |
| GET | `/health/` | Health check endpoint |

## Installation

### Prerequisites
- Python 3.11+
- Docker & docker-compose
- Git

### Local Development

1. **Clone the repository**
```bash
cd labs-monorepo/url-shortener
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

3. **Run with Docker**
```bash
docker-compose up --build
```

4. **Access the application**
- API: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

## Usage

### Create Short URL
```bash
curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/very/long/url"}'
```

### Access Short URL
```bash
curl -L http://localhost:8000/abc123
```

### Get Statistics
```bash
curl http://localhost:8000/api/stats/abc123
```

## Development

### Running Tests
```bash
docker-compose exec web python manage.py test
```

### Making Migrations
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Creating Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

## Git Workflow

This lab follows a structured Git workflow:
- Feature branches for each phase
- Pull requests to `development` branch
- Final release PR to `main` branch

## Author

Lab 1 - Django/Flask Web Fundamentals
