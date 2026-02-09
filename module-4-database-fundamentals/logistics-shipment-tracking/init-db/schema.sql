-- Lab 5: Logistics and Shipment Tracking Backend
-- Database Schema in Third Normal Form (3NF)

-- Drop existing tables if they exist
DROP TABLE IF EXISTS tracking_events CASCADE;
DROP TABLE IF EXISTS shipments CASCADE;
DROP TABLE IF EXISTS packages CASCADE;
DROP TABLE IF EXISTS facilities CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Facilities table (warehouses, distribution centers, etc.)
CREATE TABLE facilities (
    facility_id SERIAL PRIMARY KEY,
    facility_name VARCHAR(200) NOT NULL,
    facility_type VARCHAR(50) NOT NULL, -- e.g., 'warehouse', 'distribution_center', 'sorting_facility'
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    capacity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Packages table
CREATE TABLE packages (
    package_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    tracking_number VARCHAR(50) UNIQUE NOT NULL,
    weight DECIMAL(10, 2) NOT NULL,
    dimensions VARCHAR(50), -- e.g., "10x8x6"
    package_type VARCHAR(50) NOT NULL, -- e.g., 'standard', 'express', 'overnight'
    origin_facility_id INTEGER REFERENCES facilities(facility_id),
    destination_address TEXT NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    destination_state VARCHAR(50) NOT NULL,
    destination_zip VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shipments table
CREATE TABLE shipments (
    shipment_id SERIAL PRIMARY KEY,
    package_id INTEGER NOT NULL REFERENCES packages(package_id),
    current_facility_id INTEGER REFERENCES facilities(facility_id),
    status VARCHAR(50) NOT NULL, -- e.g., 'pending', 'in_transit', 'delivered', 'delayed'
    estimated_delivery TIMESTAMP,
    actual_delivery TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tracking Events table
CREATE TABLE tracking_events (
    event_id SERIAL PRIMARY KEY,
    shipment_id INTEGER NOT NULL REFERENCES shipments(shipment_id),
    facility_id INTEGER REFERENCES facilities(facility_id),
    event_type VARCHAR(100) NOT NULL, -- e.g., 'package_received', 'in_transit', 'out_for_delivery', 'delivered'
    event_description TEXT,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance optimization
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_packages_tracking ON packages(tracking_number);
CREATE INDEX idx_packages_customer ON packages(customer_id);
CREATE INDEX idx_shipments_package ON shipments(package_id);
CREATE INDEX idx_shipments_status ON shipments(status);
CREATE INDEX idx_tracking_events_shipment ON tracking_events(shipment_id);
CREATE INDEX idx_tracking_events_timestamp ON tracking_events(event_timestamp);
