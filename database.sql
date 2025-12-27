CREATE DATABASE route_management;
USE route_management;
CREATE TABLE routes (
    route_id VARCHAR(10) PRIMARY KEY,
    region VARCHAR(20),
    distance_km INT,
    vehicle_type VARCHAR(20),
    revenue DECIMAL(10,2),
    total_cost DECIMAL(10,2),
    profit DECIMAL(10,2),
    route_date DATE,
    route_json JSON
);
USE route_management;
SELECT * FROM routes LIMIT 100;
ALTER TABLE routes
ADD COLUMN total_cost INT DEFAULT 0,
ADD COLUMN profit INT DEFAULT 0;
SELECT route_id, total_cost, profit FROM routes LIMIT 10;
DESCRIBE routes;
CREATE TABLE IF NOT EXISTS route_analysis (
    route_id VARCHAR(10) PRIMARY KEY,
    is_loss BOOLEAN,
    loss_amount DECIMAL(10,2),
    profit_margin DECIMAL(10,2),
    cost_per_km DECIMAL(10,2),
    profit_per_km DECIMAL(10,2),
    is_shortest_overall BOOLEAN,
    is_shortest_region BOOLEAN,
    is_high_cost BOOLEAN,
    is_high_profit BOOLEAN,
    alert_flag BOOLEAN,
    recommended_action VARCHAR(255)
);
ALTER TABLE routes
ADD COLUMN fuel_cost DECIMAL(10,2) NULL,
ADD COLUMN toll_cost DECIMAL(10,2) NULL,
ADD COLUMN driver_cost DECIMAL(10,2) NULL,
ADD COLUMN repair_cost DECIMAL(10,2) NULL,
ADD COLUMN misc_cost DECIMAL(10,2) NULL,
ADD COLUMN loss DECIMAL(10,2) NULL,
ADD COLUMN is_profitable TINYINT(1) DEFAULT 1,
ADD COLUMN time_hours DECIMAL(10,2) NULL,
ADD COLUMN avg_speed DECIMAL(10,2) NULL,
ADD COLUMN route_efficiency_score INT NULL;
SHOW COLUMNS FROM routes;
SELECT * FROM routes LIMIT 100;




