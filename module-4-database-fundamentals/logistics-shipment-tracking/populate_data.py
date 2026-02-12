import os
import psycopg2
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def populate_bulk_data(count=100):
    """Seed the database with bulk data for performance testing."""
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'logistics_db'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASSWORD', 'admin123'),
        host=os.getenv('DB_HOST', 'localhost')
    )
    cur = conn.cursor()
    
    try:
        print(f"Generating {count} test shipments...")
        for i in range(count):
            tracking = f"TRK{random.randint(1000000, 9999999)}"
            # Insert package
            cur.execute("""
                INSERT INTO packages (customer_id, tracking_number, weight, dimensions, package_type, origin_facility_id, destination_address, destination_city, destination_state, destination_zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING package_id
            """, (random.randint(1, 5), tracking, random.uniform(0.5, 50.0), "10x10x10", "standard", random.randint(1, 5), "Dest Addr", "Dest City", "ST", "12345"))
            
            package_id = cur.fetchone()[0]
            
            # Insert shipment
            cur.execute("""
                INSERT INTO shipments (package_id, current_facility_id, status, estimated_delivery)
                VALUES (%s, %s, %s, %s)
            """, (package_id, random.randint(1, 5), "in_transit", datetime.now() + timedelta(days=3)))
            
        conn.commit()
        print("Bulk data populated successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_bulk_data(50)
