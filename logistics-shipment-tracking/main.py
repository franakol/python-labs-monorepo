import os
import psycopg2
from psycopg2 import pool
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10,
    dbname=os.getenv('DB_NAME', 'logistics_db'),
    user=os.getenv('DB_USER', 'admin'),
    password=os.getenv('DB_PASSWORD', 'admin123'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432')
)

def scan_package(tracking_number, facility_id, event_type, description):
    """
    Transactional logic for scanning a package at a facility.
    Updates the shipment status and records a tracking event.
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

                # 2. Add tracking event
                cur.execute("""
                    INSERT INTO tracking_events (shipment_id, facility_id, event_type, event_description)
                    VALUES (%s, %s, %s, %s)
                """, (shipment_id, facility_id, event_type, description))

                # 3. Update shipment status and location
                new_status = 'delivered' if event_type == 'delivered' else 'in_transit'
                
                cur.execute("""
                    UPDATE shipments 
                    SET status = %s, current_facility_id = %s, updated_at = %s
                    WHERE shipment_id = %s
                """, (new_status, facility_id, datetime.now(), shipment_id))

                print(f"Successfully processed scan for {tracking_number}: {event_type}")
                return True

    except Exception as e:
        print(f"Transaction failed: {e}")
        conn.rollback()
        return False
    finally:
        db_pool.putconn(conn)

if __name__ == "__main__":
    # Example usage
    print("Logistics Backend Scan System")
    scan_package('TRK1001234567', 2, 'in_transit', 'Package arrived at LA Sorting Facility')
