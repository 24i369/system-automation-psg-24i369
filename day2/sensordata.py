import random
import time
import csv

LOG_FILE = "day1_log.txt"
CSV_FILE = "day2_sensor_data.csv"


# STEP 1: Generate simulated sensor data
def generate_sensor_data():
    return {
        "temperature": random.randint(50, 95),
        "pressure": round(random.uniform(1.0, 5.0), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "rpm": random.randint(500, 3000),
        "current": round(random.uniform(5.0, 15.0), 2)
    }


# STEP 2: Define automation rules
RULES = [
    {
        "name": "CRITICAL_MACHINE_FAILURE",
        "priority": 1,
        "condition": lambda r: r["temperature"] > 80 and r["vibration"] > 3.5,
        "action": "EMERGENCY_STOP"
    },
    {
        "name": "OVERHEATING_PRESSURE_RISK",
        "priority": 2,
        "condition": lambda r: r["temperature"] > 80 and r["pressure"] > 4.0,
        "action": "EMERGENCY_STOP"
    },
    {
        "name": "MOTOR_OVERLOAD",
        "priority": 3,
        "condition": lambda r: r["current"] > 13 and r["vibration"] > 3.5,
        "action": "REDUCE_LOAD"
    },
    {
        "name": "EMERGENCY_HIGH_TEMP",
        "priority": 4,
        "condition": lambda r: r["temperature"] > 90,
        "action": "EMERGENCY_STOP"
    },
    {
        "name": "HIGH_VIBRATION",
        "priority": 5,
        "condition": lambda r: r["vibration"] > 4.0,
        "action": "STOP_MACHINE"
    },
    {
        "name": "HIGH_CURRENT",
        "priority": 6,
        "condition": lambda r: r["current"] > 13,
        "action": "REDUCE_LOAD"
    },
    {
        "name": "HIGH_TEMPERATURE",
        "priority": 7,
        "condition": lambda r: r["temperature"] > 80,
        "action": "COOL_MACHINE"
    },
    {
        "name": "HIGH_PRESSURE",
        "priority": 8,
        "condition": lambda r: r["pressure"] > 4.0,
        "action": "CHECK_PRESSURE"
    }
]


# STEP 3: Evaluate automation rules
def evaluate_rules(reading, rules):
    sorted_rules = sorted(rules, key=lambda r: r["priority"])

    for rule in sorted_rules:
        if rule["condition"](reading):
            return rule["name"], rule["action"]

    return "NO_RULE_FIRED", "CONTINUE_NORMAL"


# STEP 4: Take action
def take_action(action):
    actions = {
        "EMERGENCY_STOP": "Emergency stop activated!",
        "STOP_MACHINE": "Machine stopped due to unsafe condition.",
        "REDUCE_LOAD": "Machine load reduced.",
        "COOL_MACHINE": "Cooling system activated.",
        "CHECK_PRESSURE": "Pressure is high. Inspection required.",
        "CONTINUE_NORMAL": "Machine operating normally."
    }

    return actions.get(action, f"No handler for action: {action}")


# STEP 5: Log every decision in a text file
def log_decision(reading, rule_name, action, recovery):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"Reading: {reading} | "
            f"Rule: {rule_name} | "
            f"Action: {action} | "
            f"Recovery: {recovery}\n"
        )


# STEP 6: Determine machine state
def get_machine_state(action):
    if action in ["EMERGENCY_STOP", "STOP_MACHINE"]:
        return "STOPPED"

    elif action in ["REDUCE_LOAD", "COOL_MACHINE", "CHECK_PRESSURE"]:
        return "WARNING"

    return "NORMAL"


# STEP 7: Self-recovery logic
def self_recovery(reading, action):
    if action in ["EMERGENCY_STOP", "STOP_MACHINE"]:
        if (
            reading["temperature"] < 70
            and reading["pressure"] < 3.5
            and reading["vibration"] < 2.5
            and reading["current"] < 10
        ):
            return "MACHINE_RECOVERED - Restarting automatically"

        return "MACHINE_STILL_UNSAFE - Keep machine stopped"

    return "NO_RECOVERY_NEEDED"


# STEP 8: Save sensor data to CSV
def save_to_csv(reading, state, writer):
    writer.writerow({
        "temperature": reading["temperature"],
        "pressure": reading["pressure"],
        "vibration": reading["vibration"],
        "rpm": reading["rpm"],
        "current": reading["current"],
        "state": state
    })


# MAIN PROGRAM
def main():
    fieldnames = [
        "temperature",
        "pressure",
        "vibration",
        "rpm",
        "current",
        "state"
    ]

    # Create CSV and write the column headings
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Generate and process 10 sensor readings
        for tick in range(1, 251):
            reading = generate_sensor_data()

            rule_name, action = evaluate_rules(reading, RULES)
            outcome = take_action(action)
            recovery = self_recovery(reading, action)
            state = get_machine_state(action)

            print(f"[Tick {tick:02d}] SENSE -> {reading}")
            print(f"           THINK -> {rule_name}")
            print(f"           ACT   -> {outcome}")
            print(f"           STATE -> {state}")
            print(f"           RECOVERY -> {recovery}\n")

            log_decision(reading, rule_name, action, recovery)
            save_to_csv(reading, state, writer)

            time.sleep(0.2)

    print(f"Sensor data saved successfully to {CSV_FILE}")


if __name__ == "__main__":
    main()
