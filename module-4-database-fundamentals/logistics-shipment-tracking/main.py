import os
import psycopg2
import redis
import json
from pymongo import MongoClient
from psycopg2 import pool
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection pool (PostgreSQL)
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10,
    dbname=os.getenv('DB_NAME', 'logistics_db'),
    user=os.getenv('DB_USER', 'admin'),
    password=os.getenv('DB_PASSWORD', 'admin123'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432')
)

# Redis client for caching
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=0,
    decode_responses=True
)

# MongoDB client for audit logging
mongo_client = MongoClient(
    os.getenv('MONGO_URI', 'mongodb://admin:admin123@localhost:27017/')
)
audit_log = mongo_client.logistics_db.audit_logs

def scan_package(tracking_number, facility_id, event_type, description):
    """
    Transactional logic for scanning a package at a facility.
    Updates the shipment status, records a tracking event,
    caches the status in Redis, and logs to MongoDB.
    """
    conn = db_pool.getconn()
    try:
        with conn:
            with conn.cursor() as cur:
                # 1. Get package and shipment info
                cur.execute("""
                    SELECT s.shipment_id, s.status 
                    FROM packages p
                    JOIN shipments s ON p.package_id = s.package_id
                    WHERE p.tracking_number = %s
                """, (tracking_number,))
                
                result = cur.fetchone()
                if not result:
                    print(f"Error: Tracking number {tracking_number} not found.")
                    return False
                
                shipment_id, current_status = result

                # 2. Add tracking event to PostgreSQL
                cur.execute("""
                    INSERT INTO tracking_events (shipment_id, facility_id, event_type, event_description)
                    VALUES (%s, %s, %s, %s)
                """, (shipment_id, facility_id, event_type, description))

                # 3. Update shipment status and location in PostgreSQL
                new_status = 'delivered' if event_type == 'delivered' else 'in_transit'
                
                cur.execute("""
                    UPDATE shipments 
                    SET status = %s, current_facility_id = %s, updated_at = %s
                    WHERE shipment_id = %s
                """, (new_status, facility_id, datetime.now(), shipment_id))

                # 4. Cache status in Redis (TTL 1 hour)
                status_data = {
                    'status': new_status,
                    'last_facility': facility_id,
                    'timestamp': datetime.now().isoformat()
                }
                redis_client.setex(f"tracking:{tracking_number}", 3600, json.dumps(status_data))

                # 5. Log audit trail to MongoDB
                audit_log.insert_one({
                    'tracking_number': tracking_number,
                    'shipment_id': shipment_id,
                    'event': event_type,
                    'facility': facility_id,
                    'server_timestamp': datetime.utcnow()
                })

                print(f"Successfully processed scan for {tracking_number}: {event_type}")
                return True

    except Exception as e:
        print(f"Transaction failed: {e}")
        conn.rollback()
        return False
    finally:
        db_pool.putconn(conn)

def get_cached_status(tracking_number):
    """Retrieves status from Redis cache."""
    cached = redis_client.get(f"tracking:{tracking_number}")
    if cached:
        return json.loads(cached)
    return None

if __name__ == "__main__":
    # Example usage
    print("Logistics Backend Scan System (with NoSQL)")
    scan_package('TRK1001234567', 2, 'in_transit', 'Package arrived at LA Sorting Facility')
    print("Cached Status:", get_cached_status('TRK1001234567'))
