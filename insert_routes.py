import mysql.connector
import json

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Saraswathi99*",
    database="route_management"
)
cursor = conn.cursor()

# Load JSON file
with open("regional_road_express.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for route in data:

    # --- COST CALCULATION (AUTO FILL IF MISSING) ---
    fuel = route.get("fuel_cost")
    toll = route.get("toll_cost")
    driver = route.get("driver_cost")
    repair = route.get("repair_cost")
    misc = route.get("misc_cost")

    # AUTO default values if missing
    if fuel is None:
        fuel = route["distance_km"] * 5   # Example fuel rate
    if toll is None:
        toll = 100
    if driver is None:
        driver = 500
    if repair is None:
        repair = 200
    if misc is None:
        misc = 150

    total_cost = fuel + toll + driver + repair + misc
    revenue = route.get("revenue", 0)

    # --- PROFIT / LOSS ---
    profit = revenue - total_cost

    # FIXED LOSS: store ONLY positive loss value
    loss = abs(profit) if profit < 0 else 0

    is_profitable = 1 if profit >= 0 else 0

    # --- TIME & SPEED ---
    distance = route.get("distance_km", 1)

    avg_speed = route.get("avg_speed", 40)       # default speed
    time_hours = round(distance / avg_speed, 2)  # auto calculate

    # --- EFFICIENCY SCORE ---
    route_efficiency_score = int((profit / distance) * 10) if distance else 0

    # --- JSON STORE ---
    route_json = json.dumps({
        "route_points": route["route_points"],
        "vehicle": route["vehicle_type"],
        "profit": profit,
        "expenses": total_cost,
        "time_hours": time_hours,
        "avg_speed": avg_speed
    })

    # --- INSERT QUERY ---
    cursor.execute("""
        INSERT INTO routes
        (route_id, region, distance_km, vehicle_type, revenue,
         total_cost, profit, loss, fuel_cost, toll_cost, driver_cost,
         repair_cost, misc_cost, time_hours, avg_speed,
         route_efficiency_score, route_date, route_json, is_profitable)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            region = VALUES(region),
            distance_km = VALUES(distance_km),
            vehicle_type = VALUES(vehicle_type),
            revenue = VALUES(revenue),
            total_cost = VALUES(total_cost),
            profit = VALUES(profit),
            loss = VALUES(loss),
            fuel_cost = VALUES(fuel_cost),
            toll_cost = VALUES(toll_cost),
            driver_cost = VALUES(driver_cost),
            repair_cost = VALUES(repair_cost),
            misc_cost = VALUES(misc_cost),
            time_hours = VALUES(time_hours),
            avg_speed = VALUES(avg_speed),
            route_efficiency_score = VALUES(route_efficiency_score),
            route_date = VALUES(route_date),
            route_json = VALUES(route_json),
            is_profitable = VALUES(is_profitable)
    """, (
        route["route_id"],
        route["region"],
        distance,
        route["vehicle_type"],
        revenue,
        total_cost,
        profit,
        loss,
        fuel,
        toll,
        driver,
        repair,
        misc,
        time_hours,
        avg_speed,
        route_efficiency_score,
        route.get("route_date", None),
        route_json,
        is_profitable
    ))

conn.commit()
cursor.close()
conn.close()

print(f"All {len(data)} routes inserted successfully!")
