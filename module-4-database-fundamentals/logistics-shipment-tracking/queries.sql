-- Lab 5: Logistics and Shipment Tracking Backend
-- Performance Optimized Queries

-- 1. Full Tracking History for a Package
-- Optimized using idx_tracking_events_shipment
SELECT 
    p.tracking_number,
    te.event_type,
    te.event_description,
    te.event_timestamp,
    f.facility_name,
    f.city as facility_city
FROM packages p
JOIN shipments s ON p.package_id = s.package_id
JOIN tracking_events te ON s.shipment_id = te.shipment_id
LEFT JOIN facilities f ON te.facility_id = f.facility_id
WHERE p.tracking_number = 'TRK1001234567'
ORDER BY te.event_timestamp DESC;

-- 2. Shipment Throughput by Facility
-- Aggregated report for facility efficiency
SELECT 
    f.facility_name,
    f.facility_type,
    COUNT(te.event_id) as total_scans,
    COUNT(DISTINCT s.package_id) as unique_packages
FROM facilities f
JOIN tracking_events te ON f.facility_id = te.facility_id
JOIN shipments s ON te.shipment_id = s.shipment_id
GROUP BY f.facility_id, f.facility_name, f.facility_type
ORDER BY total_scans DESC;

-- 3. Delayed Shipments Report
-- Identifies packages past their estimated delivery date
SELECT 
    p.tracking_number,
    c.first_name || ' ' || c.last_name as customer_name,
    s.status,
    s.estimated_delivery,
    EXTRACT(DAY FROM (NOW() - s.estimated_delivery)) as days_delayed
FROM shipments s
JOIN packages p ON s.package_id = p.package_id
JOIN customers c ON p.customer_id = c.customer_id
WHERE s.status NOT IN ('delivered', 'cancelled')
AND s.estimated_delivery < NOW()
ORDER BY days_delayed DESC;

-- 4. Customer Shipment Summary
-- Business Intelligence query for customer engagement
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(p.package_id) as total_packages_sent,
    SUM(p.weight) as total_weight_shipped
FROM customers c
LEFT JOIN packages p ON c.customer_id = p.customer_id
GROUP BY c.customer_id
HAVING COUNT(p.package_id) > 0
ORDER BY total_packages_sent DESC;
