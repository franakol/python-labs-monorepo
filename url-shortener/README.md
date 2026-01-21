# Django URL Shortener Microservice

A production-ready URL shortener microservice built with Django REST Framework featuring Redis caching, OpenAPI documentation, and Docker containerization.

## Features

- **REST API**: Create short URLs and redirect to original URLs
- **Redis Storage**: High-performance Redis backend for URL mappings
- **OpenAPI Documentation**: Interactive Swagger UI for API testing
- **Click Analytics**: Track URL usage statistics
- **Docker**: Fully containerized with docker-compose
- **Production-Ready**: Gunicorn WSGI server, CORS support, security headers

## Architecture

### Technology Stack
- **Django 5.0+** - Web framework
- **Django REST Framework** - API development
- **drf-spectacular** - OpenAPI/Swagger documentation
- **Redis** - Primary data storage
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
│   ├── urls.py             # URL routing with Swagger
│   └── wsgi.py
├── shortener/              # Main app
│   ├── models.py           # URL model (optional backup)
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── services.py         # Business logic with Redis
│   ├── admin.py            # Django admin config
│   └── urls.py             # App URL routing
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shorten/` | Create short URL |
| GET | `/<short_code>` | Redirect to original URL (302) |
| GET | `/api/stats/<short_code>` | Get URL statistics |
| GET | `/api/docs/` | Swagger UI documentation |
| GET | `/api/schema/` | OpenAPI schema |
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
- API: http://localhost:8000/
- Swagger UI: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

## Usage

### Create Short URL
```bash
curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/very/long/url"}'
```

Response:
```json
{
  "short_code": "aB3xYz",
  "original_url": "https://example.com/very/long/url",
  "short_url": "http://localhost:8000/aB3xYz",
  "created": true
}
```

### Create Custom Short URL
```bash
curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com/page",
    "custom_code": "mylink"
  }'
```

### Access Short URL
```bash
curl -L http://localhost:8000/aB3xYz
# Redirects to original URL (HTTP 302)
```

### Get Statistics
```bash
curl http://localhost:8000/api/stats/aB3xYz
```

Response:
```json
{
  "short_code": "aB3xYz",
  "original_url": "https://example.com/very/long/url",
  "clicks": 42,
  "short_url": "http://localhost:8000/aB3xYz"
}
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

### Accessing Django Shell
```bash
docker-compose exec web python manage.py shell
```

## Redis Data Structure

The service uses Redis with the following key patterns:

- `url:<short_code>` → Original URL (with 1-year TTL)
- `clicks:<short_code>` → Click count
- `reverse:<url_hash>` → Short code (prevents duplicates)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | (auto-generated) |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

## Git Workflow

This lab follows a structured Git workflow:
- Feature branches for each phase
- Pull requests to `development` branch
- Final release PR to `main` branch

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment
2. Configure `SECRET_KEY` with a strong random value
3. Set `ALLOWED_HOSTS` to your domain
4. Use `DJANGO_SETTINGS_MODULE=config.settings.production`
5. Set up SSL/TLS certificates
6. Configure Redis persistence

## Author

Lab 1 - Django/Flask Web Fundamentals
