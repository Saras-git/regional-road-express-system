from fastapi import FastAPI
import heapq
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all websites to access this API
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]   # allow all headers
)


# ----------------------------
# DATABASE CONNECTION FUNCTION
# ----------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Saraswathi99*",
        database="route_management"
    )

# ----------------------------
# 1️⃣ GET ALL LOSS ROUTES
# ----------------------------
@app.get("/routes/loss")
def get_loss_routes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM routes WHERE profit < 0")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return {"total_loss_routes": len(data), "routes": data}

# ----------------------------
# 2️⃣ GET ALL PROFIT ROUTES
# ----------------------------
@app.get("/routes/profit")
def get_profit_routes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM routes WHERE profit >= 0")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return {"total_profit_routes": len(data), "routes": data}


# ----------------------------
# 3️⃣ PROFIT SUMMARY (For Dashboard / PowerBI)
# ----------------------------
@app.get("/summary")
def summary():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            SUM(revenue) AS total_revenue,
            SUM(total_cost) AS total_cost,
            SUM(profit) AS total_profit,
            SUM(loss) AS total_loss,
            COUNT(*) AS total_routes,
            SUM(is_profitable) AS profitable_routes,
            SUM(CASE WHEN profit < 0 THEN 1 END) AS loss_routes
        FROM routes
    """)

    data = cursor.fetchone()

    cursor.close()
    conn.close()
    return data


# ----------------------------
# 4️⃣ SHORTEST PATH – DIJKSTRA
# ----------------------------

# Graph — YOU CAN MODIFY ROUTES LATER
graph = {
    "Chennai": {"Coimbatore": 214},
    "Mumbai": {"Jaipur": 211},
    "Pune": {"Ahmedabad": 242},
    "Durgapur": {"Bhubaneswar": 152},
    "Jaipur": {"Mumbai": 140},
    "Delhi": {"Ambala": 495},
    "Satara": {"Pune": 281},
    "Ambala": {"Panipat": 336},
    "Kolkata": {"Patna": 261}
}

@app.get("/shortest-path")
def shortest_path(start: str, end: str):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue
        visited.add(node)

        path = path + [node]

        if node == end:
            return {"shortest_distance": cost, "path": path}

        for neighbor, weight in graph.get(node, {}).items():
            heapq.heappush(queue, (cost + weight, neighbor, path))

    return {"error": "No path found"}


# ----------------------------
# 5️⃣ ML – Profit Prediction Placeholder
# ----------------------------
class MLInput(BaseModel):
    distance_km: float
    fuel_cost: float
    toll_cost: float
    driver_cost: float
    repair_cost: float
    misc_cost: float

@app.post("/predict/profit")
def predict_profit(data: MLInput):
    total_cost = data.fuel_cost + data.toll_cost + data.driver_cost + data.repair_cost + data.misc_cost
    predicted_revenue = (data.distance_km * 45)  # simple formula now

    predicted_profit = predicted_revenue - total_cost

    return {
        "predicted_profit": predicted_profit,
        "profit_category": "Profitable" if predicted_profit >= 0 else "Loss"
    }
@app.post("/save-prediction")
def save_prediction(data: dict):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO profit_predictions 
        (distance_km, fuel_cost, toll_cost, driver_cost, repair_cost, misc_cost, predicted_profit, profit_category)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["distance_km"],
        data["fuel_cost"],
        data["toll_cost"],
        data["driver_cost"],
        data["repair_cost"],
        data["misc_cost"],
        data["predicted_profit"],
        data["profit_category"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Saved successfully"}
   

# ----------------------------
# API RUNNING STATUS
# ----------------------------
@app.get("/")
def home():
    return {"message": "Route Management API is running 🚚📦"}
