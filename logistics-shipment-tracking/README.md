# Lab 5: Logistics and Shipment Tracking Backend

A logistics and shipment tracking system built with Python, PostgreSQL, Redis, and MongoDB.

## Project Structure

```
logistics-shipment-tracking/
├── docker-compose.yml
├── requirements.txt
├── init-db/
│   ├── schema.sql
│   └── seed.sql
├── main.py
├── populate_data.py
└── queries.sql
```

## Requirements

- Docker & Docker Compose
- Python 3.10+
- PostgreSQL 15
- Redis
- MongoDB

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

## Database Schema

The database follows Third Normal Form (3NF) design principles with the following entities:
- Customers
- Packages
- Facilities
- Shipments
- Tracking Events

## Features

- Transactional package scanning
- Redis caching for performance
- MongoDB logging for audit trails
- Complex SQL queries with optimization
- Performance indexing

## License

MIT
