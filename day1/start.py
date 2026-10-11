"""
DAY 1 · HANDS-ON — Build Your Rule Engine
23IF02 System Automation

Work through the TODOs in order. Each one matches a step on the
"Hands-on · Build Your Rule Engine" slide. Run this file after each
step to see your progress:

   python hands_on_starter.py

Need the answer? See hands_on_solution.py — but try it yourself first.
"""

import random
import time

LOG_FILE = "day1_log.txt"


# ---------------------------------------------------------------------------
# STEP 1 — Generate simulated sensor data
# ---------------------------------------------------------------------------
def generate_sensor_data():
    """Return a dict with at least 'temperature', 'pressure', 'vibration'."""

    # Generate realistic random sensor values
    return {
        "temperature": random.randint(50, 95),       # Temperature in degrees C
        "pressure": round(random.uniform(1.0, 5.0), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "current": round(random.uniform(5.0, 15.0), 2)
            }

    # STRETCH GOAL (after the 8 steps below all work): real sensors aren't
    # perfectly clean. Try making one field randomly return None (a
    # dropout) or spike far outside its normal range every so often, then
    # update evaluate_rules() so a dropout doesn't crash your engine.


# ---------------------------------------------------------------------------
# STEP 2 — Write your first automation rules
# STEP 7 — Add a rule of your own (add another dict to this list)
# STEP 8 — Add one priority rule (lower "priority" number checked first)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# STEP 3 — Detect machine state from the rules
# ---------------------------------------------------------------------------
def evaluate_rules(reading, rules):
    """
    Return (rule_name, action) for the first matching rule.
    Rules are checked in priority order.
    """

    # Sort rules by priority; the lowest number is checked first
    sorted_rules = sorted(rules, key=lambda r: r["priority"])

    # Check each rule against the current sensor readings
    for rule in sorted_rules:
        if rule["condition"](reading):
            return rule["name"], rule["action"]

    # If no rule matches, continue normal operation
    return "NO_RULE_FIRED", "CONTINUE_NORMAL"


# ---------------------------------------------------------------------------
# STEP 4 — Trigger an action when a rule fires
# ---------------------------------------------------------------------------
def take_action(action):
    """Return a human-readable message for the action."""

    # Map each action name to its message
    actions = {
        "EMERGENCY_STOP": "Emergency stop activated!",
        "STOP_MACHINE": "Machine stopped due to unsafe condition.",
        "REDUCE_LOAD": "Machine load reduced.",
        "COOL_MACHINE": "Cooling system activated.",
        "CHECK_PRESSURE": "Pressure is high. Inspection required.",
        "CONTINUE_NORMAL": "Machine operating normally."
    }

    # Return the message for the action
    return actions.get(action, f"No handler for action: {action}")


# ---------------------------------------------------------------------------
# STEP 5 — Log every decision made
# ---------------------------------------------------------------------------
def log_decision(reading, rule_name, action,recovery):
    """Append one line to the log file."""

    # Open the log file in append mode and write the decision
    with open(LOG_FILE, "a") as file:
        file.write(
            f"Reading: {reading} | "
            f"Rule: {rule_name} | "
            f"Action: {action} | "
            f"Recovery: {recovery}\n"
        )


# ---------------------------------------------------------------------------
# STEP 6 — Add a second sensor to the system
# Current is added as an extra sensor in generate_sensor_data().
# It is also used by the MOTOR_OVERLOAD and HIGH_CURRENT rules.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# STEP 7 & 8 — Additional rules and priority rules
# These are included in the RULES list above.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# STEP 9 — Add self-recovery logic
# ---------------------------------------------------------------------------
def self_recovery(reading, action):
    """Check whether the machine readings are safe for recovery."""

    # Recovery is checked only if the machine was stopped
    if action in ["EMERGENCY_STOP", "STOP_MACHINE"]:

        # Check whether all sensor readings are within safe limits
        if (
            reading["temperature"] < 70
            and reading["pressure"] < 3.5
            and reading["vibration"] < 2.5
            and reading["current"] < 10
        
        ):
            return "MACHINE_RECOVERED - Restarting automatically"

        else:
            return "MACHINE_STILL_UNSAFE - Keep machine stopped"

    # No recovery check is needed for other actions
    return "NO_RECOVERY_NEEDED"


# ---------------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------------
def main():

    # Run the automation system for 10 ticks
    for tick in range(1, 11):
        reading = generate_sensor_data()
        rule_name, action = evaluate_rules(reading, RULES)
        outcome = take_action(action)
        recovery = self_recovery(reading, action)
        print(f"[Tick {tick:02d}] SENSE -> {reading}")
        print(f"           THINK -> {rule_name}")
        print(f"           ACT   -> {outcome}")
        print(f"           RECOVERY -> {recovery}\n")
        log_decision(reading, rule_name, action,recovery)
        time.sleep(0.2)


if __name__ == "__main__":
    main()