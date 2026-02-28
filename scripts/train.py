import pandas as pd
import os
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor


# ==============================
# Create outputs directory
# ==============================
os.makedirs("outputs", exist_ok=True)


# ==============================
# Load Dataset
# ==============================
data = pd.read_csv("dataset/winequality-red.csv", sep=';')

target = "quality"
X = data.drop(target, axis=1)
y = data[target]


# ==============================
# Preprocessing (Scaling)
# ==============================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# ==============================
# Train-Test Split
# ==============================
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=test_size, random_state=42
)


# ==============================
# Model Training
# ==============================
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    random_state=42
)

model.fit(X_train, y_train)


# ==============================
# Prediction
# ==============================
y_pred = model.predict(X_test)


# ==============================
# Evaluation Metrics
# ==============================
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


print("===== Model Training Completed =====")
print(f"MSE: {mse}")
print(f"R2: {r2}")


# ==============================
# Save Model and Scaler
# ==============================
joblib.dump(model, "outputs/model.pkl")
joblib.dump(scaler, "outputs/scaler.pkl")


# ==============================
# Save Clean Metrics JSON
# ==============================
metrics = {
    "mse": mse,
    "r2": r2
}

with open("outputs/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)


print("Model, scaler, and metrics saved successfully.")