-- Seed data for Logistics and Shipment Tracking Database

-- Insert sample customers
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES
('John', 'Doe', 'john.doe@example.com', '555-0101', '123 Main St', 'New York', 'NY', '10001'),
('Jane', 'Smith', 'jane.smith@example.com', '555-0102', '456 Oak Ave', 'Los Angeles', 'CA', '90001'),
('Bob', 'Johnson', 'bob.johnson@example.com', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60601'),
('Alice', 'Williams', 'alice.williams@example.com', '555-0104', '321 Elm St', 'Houston', 'TX', '77001'),
('Charlie', 'Brown', 'charlie.brown@example.com', '555-0105', '654 Maple Dr', 'Phoenix', 'AZ', '85001');

-- Insert sample facilities
INSERT INTO facilities (facility_name, facility_type, address, city, state, zip_code, capacity) VALUES
('NYC Distribution Center', 'distribution_center', '100 Warehouse Blvd', 'New York', 'NY', '10002', 50000),
('LA Sorting Facility', 'sorting_facility', '200 Logistics Ave', 'Los Angeles', 'CA', '90002', 30000),
('Chicago Warehouse', 'warehouse', '300 Storage St', 'Chicago', 'IL', '60602', 40000),
('Houston Hub', 'distribution_center', '400 Delivery Ln', 'Houston', 'TX', '77002', 35000),
('Phoenix Terminal', 'sorting_facility', '500 Transit Way', 'Phoenix', 'AZ', '85002', 25000);

-- Insert sample packages
INSERT INTO packages (customer_id, tracking_number, weight, dimensions, package_type, origin_facility_id, destination_address, destination_city, destination_state, destination_zip) VALUES
(1, 'TRK1001234567', 5.50, '12x10x8', 'standard', 1, '456 Oak Ave', 'Los Angeles', 'CA', '90001'),
(2, 'TRK1001234568', 3.25, '8x6x4', 'express', 2, '789 Pine Rd', 'Chicago', 'IL', '60601'),
(3, 'TRK1001234569', 8.75, '16x12x10', 'overnight', 3, '321 Elm St', 'Houston', 'TX', '77001'),
(4, 'TRK1001234570', 2.10, '6x4x3', 'standard', 4, '654 Maple Dr', 'Phoenix', 'AZ', '85001'),
(5, 'TRK1001234571', 6.40, '14x10x6', 'express', 5, '123 Main St', 'New York', 'NY', '10001');

-- Insert sample shipments
INSERT INTO shipments (package_id, current_facility_id, status, estimated_delivery) VALUES
(1, 1, 'in_transit', NOW() + INTERVAL '3 days'),
(2, 2, 'in_transit', NOW() + INTERVAL '1 day'),
(3, 3, 'pending', NOW() + INTERVAL '12 hours'),
(4, 4, 'delivered', NOW() - INTERVAL '1 day'),
(5, 5, 'in_transit', NOW() + INTERVAL '2 days');

-- Insert sample tracking events
INSERT INTO tracking_events (shipment_id, facility_id, event_type, event_description) VALUES
(1, 1, 'package_received', 'Package received at NYC Distribution Center'),
(1, 1, 'in_transit', 'Package departed NYC Distribution Center'),
(2, 2, 'package_received', 'Package received at LA Sorting Facility'),
(2, 2, 'in_transit', 'Package sorted and ready for dispatch'),
(3, 3, 'package_received', 'Package received at Chicago Warehouse'),
(4, 4, 'package_received', 'Package received at Houston Hub'),
(4, 4, 'out_for_delivery', 'Package out for delivery'),
(4, 4, 'delivered', 'Package successfully delivered'),
(5, 5, 'package_received', 'Package received at Phoenix Terminal');
