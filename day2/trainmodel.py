
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Get the folder containing this Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load sensor dataset
CSV_PATH = os.path.join(BASE_DIR, "day2_sensor_data.csv")
df = pd.read_csv(CSV_PATH)

# Input features
features = [
    "temperature",
    "pressure",
    "vibration",
    "rpm",
    "current"
]

# Output label
target = "state"

# Prepare data
df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

# Train model
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)

print("Model: Random Forest")
print("Total records:", len(df))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Save trained model
MODEL_PATH = os.path.join(BASE_DIR, "random_forest_model.pkl")
joblib.dump(model, MODEL_PATH)

print("\nRandom Forest model saved successfully!")
print("Saved at:", MODEL_PATH)

# Example prediction
sample = pd.DataFrame([{
    "temperature": 75,
    "pressure": 3.0,
    "vibration": 2.0,
    "rpm": 1500,
    "current": 10.0
}])

prediction = model.predict(sample)

print("\nSample sensor reading:")
print(sample)
print("Predicted machine state:", prediction[0])